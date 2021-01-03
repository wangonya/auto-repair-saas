echo "making migrations ..."
python manage.py makemigrations
echo "running migrations ..."
python manage.py migrate
echo "done"