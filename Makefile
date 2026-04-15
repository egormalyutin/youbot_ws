.PHONY: clean build-host build-youbot build upload

clean:
	rm -rf targets

build-host:
	mkdir -p targets/host/log
	mkdir -p targets/host/build
	mkdir -p targets/host/install

	colcon --log-base targets/host/log build \
		--base-paths ./ \
		--build-base targets/host/build \
		--install-base targets/host/install \
		--symlink-install \
		--cmake-args '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON'

build-youbot:
	mkdir -p targets/youbot/log
	mkdir -p targets/youbot/build
	mkdir -p targets/youbot/install

	colcon --log-base targets/youbot/log build \
		--base-paths ./ \
		--build-base targets/youbot/build \
		--install-base targets/youbot/install \
		--packages-select brics_actuator youbot_description youbot_driver youbot_driver_ros_interface

build: build-host build-youbot

upload: build-youbot
	rsync -avz --delete targets/youbot/install/ youbot:ros2_install_dir
