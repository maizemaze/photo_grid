cd ~/Dropbox/photo_grid
# Compile
sudo rm -rf dist build
# sudo pip3 install bleach --upgrade
sudo python3 setup.py sdist bdist_wheel

# Test it FIRST
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
cd
sudo python3 -m pip install --index-url https://test.pypi.org/simple --no-deps ZZLab_James --upgrade

# Upload to the real PyPI
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
cd
sudo python3 -m pip install photo_grid --upgrade



# l /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/ZZLab_James
# cd /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/ZZLab_James/
