sudo apt-get install python3 python3-pip
pip3 uninstall -y pygame
sudo apt-get update
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-setuptools python3-dev libportmidi-dev
sudo apt-get build-dep libsdl2 libsdl2-image libsdl2-mixer libsdl2-ttf libfreetype6 python3 libportmidi0
python3 dependencies/pygame/setup.py -config -auto -sdl2
python3 dependencies/pygame/setup.py install --user
echo "alias visualizer='python3 $(pwd)/src/main.py'" >> ~/.bash_aliases