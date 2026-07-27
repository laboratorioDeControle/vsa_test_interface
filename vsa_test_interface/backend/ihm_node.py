import math
from rclpy.node import Node
from ..frontend.ihm_main_window import IHMWindow
from .tools import calculate_calibration_parameters

from nav_msgs.msg import Odometry
from std_msgs.msg import Empty, UInt8MultiArray, Float64MultiArray

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
        self.teleoperation_pub = None

        self._last_odometry_msg_stamp_ns: int = 0
        self._odometry_dt: float = 0.0

        self.send_motors_timer = self.create_timer(1.0, self.send_motors_command)
        self.send_motors_timer.cancel()

        self.__init_ui_integration__()

    def __init_ui_integration__(self):
        self._main_window.main_widget.com_topics.bt_start_sampling.clicked.connect(self.__bt_start_stop_topics_com_callback__)
        self._main_window.main_widget.mission.bt_send_mission_parameters.clicked.connect(self.__bt_send_auto_mission_callback__)

        self._main_window.main_widget.mission.manual_mission_widget.bt_send_command.clicked.connect(self.send_motors_start_periodic)
        self._main_window.main_widget.mission.payload_test_widget.bt_send_command.clicked.connect(self.send_led_command)

        self._main_window.main_widget.mission.payload_test_widget.relay_1.stateChanged.connect(self.send_relay_command)
        self._main_window.main_widget.mission.payload_test_widget.relay_2.stateChanged.connect(self.send_relay_command)
        self._main_window.main_widget.mission.payload_test_widget.relay_3.stateChanged.connect(self.send_relay_command)

        self._main_window.main_widget.calibration.calib_thruster.bt_start_stop_experiment.clicked.connect(self.start_stop_thruster_calib_point)
        self._main_window.main_widget.calibration.calib_thruster.bt_calculate.clicked.connect(self.calculate_thruster_calibration)
    

    def __bt_start_stop_topics_com_callback__(self):
        self._is_connected = not self._is_connected
        self._main_window.main_widget.com_topics.start_stop_comunication(self._is_connected)

        odometry_topic: str = self._main_window.main_widget.com_topics.odometry_topic
        heart_beat_topic: str = self._main_window.main_widget.com_topics.heart_beat_topic
        can_topic: str = self._main_window.main_widget.com_topics.can_bus_topic

        plan_db_topic: str = "/plan_db"

        if not self._is_connected:            
            self._last_odometry_msg_stamp_ns = 0
            self._odometry_dt = 0.0

        else:
            if self._sub_odometry == None:
                self._sub_odometry = self.create_subscription(Odometry, odometry_topic, self.__topic_odometry_callback__, 10)
                self._sub_heart_beat = self.create_subscription(Empty, heart_beat_topic, self.__topic_heart_beat_callback__, 10)
                self._pub_plan_db = self.create_publisher(PlanDB, plan_db_topic, 10)
                self._pub_can = self.create_publisher(UInt8MultiArray, can_topic, 10)
                self.teleoperation_pub = self.create_publisher(Float64MultiArray, '/teleoperation', 10)

            self._main_window.main_widget.xy_graph.clear()
            self._main_window.main_widget.speed_graph.clear()

    def __bt_send_auto_mission_callback__(self):
        if self._main_window.main_widget.mission.is_autonomous_mission:
            mission_time: float = self._main_window.main_widget.mission.autonomous_mission_widget.mission_time
            mission_start_delay: float = self._main_window.main_widget.mission.autonomous_mission_widget.mission_start_delay
            thruster_power: float = self._main_window.main_widget.mission.autonomous_mission_widget.thruster_power
            vertical_rudders: float = self._main_window.main_widget.mission.autonomous_mission_widget.vertical_rudders_angle
            horizontal_rudders: float = self._main_window.main_widget.mission.autonomous_mission_widget.horizontal_rudders_angle
            cycles_frequency: float = self._main_window.main_widget.mission.autonomous_mission_widget.cycle_frequency

            msg: PlanDB = PlanDB()
            msg_plan_maneuver: PlanManeuver = PlanManeuver()
            msg_maneuver: Maneuver = Maneuver()

            # VSA Test Maneuver Id
            msg_maneuver.maneuver_imc_id = 900
            msg_maneuver.maneuver_name = "VSA Test Maneuver"
            msg_maneuver.mission_time = mission_time
            msg_maneuver.mission_start_delay = mission_start_delay
            msg_maneuver.thruster_power = thruster_power
            msg_maneuver.vertical_rudders_angle = (vertical_rudders * math.pi) / 180.0
            msg_maneuver.horizontal_rudders_angle = (horizontal_rudders * math.pi) / 180.0
            msg_maneuver.cycle_frequency = cycles_frequency

            msg_plan_maneuver.maneuver_id = str(msg_maneuver.maneuver_imc_id)
            msg_plan_maneuver.maneuver = msg_maneuver

            msg.op = 9
            msg.plan_spec.maneuvers.append(msg_plan_maneuver)

            self._pub_plan_db.publish(msg)
            print("send auto mission")


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

    def send_motors_start_periodic(self):
        periodic_send: bool = self._main_window.main_widget.mission.manual_mission_widget.periodic_send

        if periodic_send:
            send_started: bool = self._main_window.main_widget.mission.manual_mission_widget.send_started

            if not send_started:
                period: float = self._main_window.main_widget.mission.manual_mission_widget.send_period
                self.send_motors_timer = self.create_timer(period, self.send_motors_command)
                self._main_window.main_widget.mission.manual_mission_widget.send_started = True

            else:
                self.send_motors_timer.cancel()
                self._main_window.main_widget.mission.manual_mission_widget.send_started = False

        else:
            self.send_motors_command()

    def send_motors_command(self):
        msg = UInt8MultiArray()
        msg.data = self._main_window.main_widget.mission.manual_mission_widget.motors_msg
        self._pub_can.publish(msg)

        print("[Motors] -> " , self._main_window.main_widget.mission.manual_mission_widget.motors_msg)

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
                teleop_msg_list[1] = parameters["power"] / 100.0
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

            self._main_window.main_widget.mission.autonomous_mission_widget.thruster_calib = calibration_parameters["interpolation_poly_coef"]
