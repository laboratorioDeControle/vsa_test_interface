from setuptools import find_packages, setup

package_name = 'vsa_test_interface'
frontend_modules: str = "vsa_test_interface/frontend"
backend_modules: str = "vsa_test_interface/backend"

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']) + [frontend_modules, backend_modules],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='laboratoriodecontrole@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'vsa_test_interface = vsa_test_interface.test_interface:main'
        ],
    },
)
