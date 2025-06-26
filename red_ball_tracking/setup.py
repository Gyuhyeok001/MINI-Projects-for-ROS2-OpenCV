from setuptools import setup

package_name = 'red_ball_tracking'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Red Ball tracking node using ROS2 and OpenCV',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'color_pub = red_ball_tracking.color_pub_node:main',
        ],
    },
)
