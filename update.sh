git reset --hard origin/main
git checkout main
git pull
echo "y" | python3 -m  pip uninstall Orise_Twin_Rotor
cd Library
python3 -m build
python3 -m pip install dist/*.whl
echo "All done and updated"