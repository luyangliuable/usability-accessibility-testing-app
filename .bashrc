export REDIS_URL="redis://127.0.0.1:6379/0"
export REDIS_BACKEND="redis://"
export LOCAL_FLASK="http://127.0.0.1:5000"
export celerystart="celery worker --app=tasks.celery --loglevel=info"
alias cleardockercontainer="docker ps -a -q | xargs docker rm -f"
alias cleardockerimage="docker image ls -a -q | xargs docker image rm -f"
alias start_flask_backend="python3 manage.py run -h localhost -p 5005"
alias start_redis_inside_docker="docker-compose up -d redis"
alias ls3="aws --endpoint-url=http://localhost:4566 s3 ls"

export S3_URL=http://localhost:4566
export FLASK_DEBUG=1
