uv export -o requirements.txt

pip install -r requirements.txt -t dependencies/python --platform manylinux2014_x86_64 --only-binary=:all: