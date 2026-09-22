import math
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType
from ..frontend.ihm_main_window import IHMWindow
from .tools import calculate_calibration_parameters

from nav_msgs.msg import Odometry
from std_msgs.msg import Empty, UInt8MultiArray, Float64MultiArray, Bool

from neptus_msgs.msg import PlanDB
from neptus_msgs.msg import PlanManeuver
from neptus_msgs.msg import Maneuver


class IHMNode(Node):
    def __init__(self, ihm_main_window: IHMWindow = None):
        super().__init__("ros2_ihm_node")
        self._main_window: IHMWindow = ihm_main_window
        self._is_connected: bool = False

        self._sub_odometry = None
        self._sub_heart_beat = None

        self._pub_plan_db = None 
        self._pub_thruster = None
        self._pub_rudders = None
        self._pub_can = None
        self._pub_abort = None
        self._pub_bag_recorder = None
        self.teleoperation_pub = None

        self._last_odometry_msg_stamp_ns: int = 0
        self._odometry_dt: float = 0.0

        self.send_motors_timer = self.create_timer(1.0, self.send_motors_command)
        self.send_motors_timer.cancel()

        # Cliente para definir parâmetros no control_node
        self._set_parameters_client = self.create_client(SetParameters, '/control_node/set_parameters')

        self.__init_ui_integration__()

    def __init_ui_integration__(self):
        self._main_window.main_widget.com_topics.bt_start_sampling.clicked.connect(self.__bt_start_stop_topics_com_callback__)
        self._main_window.main_widget.mission.bt_send_mission_parameters.clicked.connect(self.__bt_send_auto_mission_callback__)
        self._main_window.main_widget.mission.bt_abort.clicked.connect(self.__bt_abort_callback__)

        self._main_window.main_widget.mission.actuators_can_test_widget.bt_send_command.clicked.connect(self.send_motors_can_start_periodic)
        self._main_window.main_widget.mission.actuators_test_widget.bt_send_command.clicked.connect(self.send_motors_start_periodic)
        self._main_window.main_widget.mission.actuators_test_widget.bt_send_offsets.clicked.connect(self.send_offset_parameters)
        self._main_window.main_widget.mission.payload_test_widget.bt_send_command.clicked.connect(self.send_led_command)

        self._main_window.main_widget.mission.payload_test_widget.relay_1.stateChanged.connect(self.send_relay_command)
        self._main_window.main_widget.mission.payload_test_widget.relay_2.stateChanged.connect(self.send_relay_command)
        self._main_window.main_widget.mission.payload_test_widget.relay_3.stateChanged.connect(self.send_relay_command)

        self._main_window.main_widget.calibration.calib_thruster.bt_start_stop_experiment.clicked.connect(self.start_stop_thruster_calib_point)
        self._main_window.main_widget.calibration.calib_thruster.bt_calculate.clicked.connect(self.calculate_thruster_calibration)

        self._main_window.main_widget.com_topics.chb_save_bag.stateChanged.connect(self._chb_record_bag_callback)
    

    def __bt_start_stop_topics_com_callback__(self):
        self._is_connected = not self._is_connected
        self._main_window.main_widget.com_topics.start_stop_comunication(self._is_connected)

        odometry_topic: str = self._main_window.main_widget.com_topics.odometry_topic
        heart_beat_topic: str = self._main_window.main_widget.com_topics.heart_beat_topic
        can_topic: str = self._main_window.main_widget.com_topics.can_bus_topic
        thruster_topic: str = self._main_window.main_widget.com_topics.thruster_topic
        rudders_topic: str = self._main_window.main_widget.com_topics.rudders_topic
        abort_topic: str = self._main_window.main_widget.com_topics.abort_topic
        bag_recorder: str = "/bag_recorder"

        plan_db_topic: str = "/plan_db"

        if not self._is_connected:            
            self._last_odometry_msg_stamp_ns = 0
            self._odometry_dt = 0.0
            self._main_window.main_widget.com_topics.chb_save_bag.setChecked(False)

        else:
            if self._sub_odometry == None:
                self._sub_odometry = self.create_subscription(Odometry, odometry_topic, self.__topic_odometry_callback__, 10)
                self._sub_heart_beat = self.create_subscription(Empty, heart_beat_topic, self.__topic_heart_beat_callback__, 10)
                self._pub_plan_db = self.create_publisher(PlanDB, plan_db_topic, 10)
                self._pub_can = self.create_publisher(UInt8MultiArray, can_topic, 10)
                self._pub_thruster = self.create_publisher(Float64MultiArray, thruster_topic, 10)
                self._pub_rudders = self.create_publisher(Float64MultiArray, rudders_topic, 10)
                self._pub_abort = self.create_publisher(Empty, abort_topic, 10)
                self._pub_bag_recorder = self.create_publisher(Bool, bag_recorder, 10)
                self.teleoperation_pub = self.create_publisher(Float64MultiArray, '/teleoperation', 10)

            self._main_window.main_widget.xy_graph.clear()
            self._main_window.main_widget.speed_graph.clear()

    def __bt_send_auto_mission_callback__(self):
        if self._main_window.main_widget.mission.is_autonomous_mission:
            mission_parameters: dict = self._main_window.main_widget.mission.autonomous_mission_widget.mission_parameters

            msg: PlanDB = PlanDB()
            msg_plan_maneuver: PlanManeuver = PlanManeuver()
            msg_maneuver: Maneuver = Maneuver()

            # VSA Test Maneuver Id
            msg_maneuver.maneuver_imc_id = 900
            msg_maneuver.maneuver_name = "VSA Test Maneuver"

            msg_maneuver.pre_dive_time = mission_parameters["pre_dive_time"]
            msg_maneuver.pre_dive_start_delay = mission_parameters["pre_dive_start_delay"]
            msg_maneuver.pre_dive_thruster_power = mission_parameters["pre_dive_thruster_power"]
            msg_maneuver.pre_dive_vertical_rudders_angle = mission_parameters["pre_dive_vertical_rudders_angle"]
            msg_maneuver.pre_dive_horizontal_rudders_angle = mission_parameters["pre_dive_horizontal_rudders_angle"]

            msg_maneuver.dive_time = mission_parameters["dive_time"]
            msg_maneuver.dive_start_delay = mission_parameters["dive_start_delay"]
            msg_maneuver.dive_thruster_power = mission_parameters["dive_thruster_power"]
            msg_maneuver.dive_vertical_rudders_angle = mission_parameters["dive_vertical_rudders_angle"]
            msg_maneuver.dive_horizontal_rudders_angle = mission_parameters["dive_horizontal_rudders_angle"]
            msg_maneuver.dive_cycle_frequency = mission_parameters["dive_cycle_frequency"]
            msg_maneuver.dive_complete_oscilation = mission_parameters["dive_complete_oscilation"]

            msg_plan_maneuver.maneuver_id = str(msg_maneuver.maneuver_imc_id)
            msg_plan_maneuver.maneuver = msg_maneuver

            msg.op = 9
            msg.plan_spec.maneuvers.append(msg_plan_maneuver)

            self._pub_plan_db.publish(msg)
            print("send auto mission")

    def __bt_abort_callback__(self):
        msg = Empty()
        self._pub_abort.publish(msg)
        print("abort")


    def __topic_odometry_callback__(self, msg):
        if self._is_connected:
            if self._odometry_dt == 0.0:
                current_stamp_ns: int = msg.header.stamp.nanosec
                if self._last_odometry_msg_stamp_ns == 0:
                    self._last_odometry_msg_stamp_ns = current_stamp_ns
                else:
                    self._odometry_dt = float(current_stamp_ns - self._last_odometry_msg_stamp_ns) / 1000000000.0

            else:
                speed_xy: float = math.sqrt((msg.twist.twist.linear.x * msg.twist.twist.linear.x) + (msg.twist.twist.linear.y * msg.twist.twist.linear.y))
                self._main_window.main_widget.xy_graph.live_plot(msg.pose.pose.position.y, msg.pose.pose.position.x, False) # force_dx=self._odometry_dt)
                self._main_window.main_widget.speed_graph.live_plot(1.0, speed_xy, True)



    def __topic_heart_beat_callback__(self, msg):
        if self._is_connected:
            pass

    def send_motors_can_start_periodic(self):
        periodic_send: bool = self._main_window.main_widget.mission.actuators_can_test_widget.periodic_send

        if periodic_send:
            send_started: bool = self._main_window.main_widget.mission.actuators_can_test_widget.send_started

            if not send_started:
                period: float = self._main_window.main_widget.mission.actuators_can_test_widget.send_period
                self.send_motors_timer = self.create_timer(period, self.send_motors_can_command)
                self._main_window.main_widget.mission.actuators_can_test_widget.send_started = True

            else:
                self.send_motors_timer.cancel()
                self._main_window.main_widget.mission.actuators_can_test_widget.send_started = False

        else:
            self.send_motors_can_command()

    def send_motors_start_periodic(self):
        periodic_send: bool = self._main_window.main_widget.mission.actuators_test_widget.periodic_send

        if periodic_send:
            send_started: bool = self._main_window.main_widget.mission.actuators_test_widget.send_started

            if not send_started:
                period: float = self._main_window.main_widget.mission.actuators_test_widget.send_period
                self.send_motors_timer = self.create_timer(period, self.send_motors_command)
                self._main_window.main_widget.mission.actuators_test_widget.send_started = True

            else:
                self.send_motors_timer.cancel()
                self._main_window.main_widget.mission.actuators_test_widget.send_started = False

        else:
            self.send_motors_command()

    def send_motors_can_command(self):
        msg = UInt8MultiArray()
        msg.data = self._main_window.main_widget.mission.actuators_can_test_widget.motors_msg
        self._pub_can.publish(msg)

        print("[Motors] -> " , self._main_window.main_widget.mission.actuators_can_test_widget.motors_msg)

    def send_motors_command(self):
        rudders_msg = Float64MultiArray()
        rudders_msg.data = self._main_window.main_widget.mission.actuators_test_widget.rudders_msg
        
        thrusters_msg = Float64MultiArray()
        thrusters_msg.data = self._main_window.main_widget.mission.actuators_test_widget.thrusters_msg
        
        self._pub_rudders.publish(rudders_msg)
        self._pub_thruster.publish(thrusters_msg)

        print("[Rudders] -> ", self._main_window.main_widget.mission.actuators_test_widget.rudders_msg)
        print("[Thrusters] -> ", self._main_window.main_widget.mission.actuators_test_widget.thrusters_msg)

    def send_relay_command(self):
        msg = UInt8MultiArray()
        msg.data = self._main_window.main_widget.mission.payload_test_widget.relays_msg
        self._pub_can.publish(msg)

        print("[Relays] -> " , self._main_window.main_widget.mission.payload_test_widget.relays_msg)

    def send_led_command(self):
        msg = UInt8MultiArray()
        msg.data = self._main_window.main_widget.mission.payload_test_widget.leds_msg
        self._pub_can.publish(msg)

        print("[Leds] -> " , self._main_window.main_widget.mission.payload_test_widget.leds_msg)

    def start_stop_thruster_calib_point(self):
        parameters: dict = self._main_window.main_widget.calibration.calib_thruster.experiment_parameters
        exectution_experiment: bool = self._main_window.main_widget.calibration.calib_thruster.execution_experiment
        teleop_msg_list: list = [1.0, 0.0, 0.0, 0.0]
        teleop_msg: Float64MultiArray = Float64MultiArray()

        if parameters["power"] is not None:
            if not exectution_experiment:
                self._main_window.main_widget.calibration.calib_thruster.execution_experiment = True

                teleop_msg_list[1] = parameters["power"]
                teleop_msg_list[2] = parameters["vertical_rudders"]
                teleop_msg_list[3] = parameters["horizontal_rudders"]

                self._main_window.main_widget.calibration.calib_thruster.counter.zero()
                self._main_window.main_widget.calibration.calib_thruster.counter.start()
            else:
                teleop_msg_list[1] = 0.0
                self._main_window.main_widget.calibration.calib_thruster.execution_experiment = False
                self._main_window.main_widget.calibration.calib_thruster.counter.stop()
                seconds: float = float(self._main_window.main_widget.calibration.calib_thruster.counter.elapsed_seconds)
                self._main_window.main_widget.calibration.calib_thruster.measurement_table.time = seconds

            teleop_msg.data = teleop_msg_list
            self.teleoperation_pub.publish(teleop_msg)

    def send_offset_parameters(self):
        """Envia os valores de offset dos servos para o control_node via ROS2 parameter server"""
        if not self._set_parameters_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning('Serviço de parâmetros do control_node não disponível')
            return

        # Obter os valores de offset do widget
        servo_top_offset = self._main_window.main_widget.mission.actuators_test_widget.top_offset
        servo_right_offset = self._main_window.main_widget.mission.actuators_test_widget.right_offset
        servo_down_offset = self._main_window.main_widget.mission.actuators_test_widget.bottom_offset
        servo_left_offset = self._main_window.main_widget.mission.actuators_test_widget.left_offset

        # Criar a requisição com os parâmetros
        request = SetParameters.Request()
        
        # Parâmetro servo_top_offset_deg
        param1 = Parameter()
        param1.name = 'servo_top_offset_deg'
        param1.value.type = ParameterType.PARAMETER_DOUBLE
        param1.value.double_value = servo_top_offset
        
        # Parâmetro servo_right_offset_deg
        param2 = Parameter()
        param2.name = 'servo_right_offset_deg'
        param2.value.type = ParameterType.PARAMETER_DOUBLE
        param2.value.double_value = servo_right_offset
        
        # Parâmetro servo_down_offset_deg
        param3 = Parameter()
        param3.name = 'servo_down_offset_deg'
        param3.value.type = ParameterType.PARAMETER_DOUBLE
        param3.value.double_value = servo_down_offset
        
        # Parâmetro servo_left_offset_deg
        param4 = Parameter()
        param4.name = 'servo_left_offset_deg'
        param4.value.type = ParameterType.PARAMETER_DOUBLE
        param4.value.double_value = servo_left_offset
        
        request.parameters = [param1, param2, param3, param4]

        # Enviar a requisição de forma assíncrona
        future = self._set_parameters_client.call_async(request)
        future.add_done_callback(self._offset_parameters_callback)
        
        print(f"[Offsets] Enviando: Top={servo_top_offset}°, Right={servo_right_offset}°, Down={servo_down_offset}°, Left={servo_left_offset}°")

    def _offset_parameters_callback(self, future):
        """Callback para verificar se os parâmetros foram definidos com sucesso"""
        try:
            response = future.result()
            results = response.results
            
            success = all(result.successful for result in results)
            
            if success:
                self.get_logger().info('Parâmetros de offset enviados com sucesso')
            else:
                self.get_logger().warning('Alguns parâmetros de offset não foram definidos corretamente')
                for i, result in enumerate(results):
                    if not result.successful:
                        self.get_logger().warning(f'Parâmetro {i}: {result.reason}')
        except Exception as e:
            self.get_logger().error(f'Erro ao definir parâmetros de offset: {str(e)}')

    def _chb_record_bag_callback(self):
        save_bag: bool = self._main_window.main_widget.com_topics.chb_save_bag.isChecked()

        msg = Bool()
        msg.data = save_bag

        self._pub_bag_recorder.publish(msg)


    def calculate_thruster_calibration(self):
        measurements: dict = self._main_window.main_widget.calibration.calib_thruster.measurement_table.get_measurements()
        power: list = []
        speed: list = []

        if ("Potência (%)" in measurements.keys()) and ("Velocidade Média (m/s)" in measurements.keys()):
            power = measurements["Potência (%)"]
            speed = measurements["Velocidade Média (m/s)"]

            calibration_parameters: list = calculate_calibration_parameters(speed, power)
            self._main_window.main_widget.calibration.calib_thruster.result.poly = calibration_parameters["interpolation_poly_coef"]
            self._main_window.main_widget.calibration.calib_thruster.result.r2 = calibration_parameters["r2"]

            self._main_window.main_widget.mission.autonomous_mission_widget.set_thruster_calib(calibration_parameters["interpolation_poly_coef"])

