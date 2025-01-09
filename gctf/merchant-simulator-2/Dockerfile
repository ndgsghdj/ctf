FROM python:3.11-alpine

RUN apk add --no-cache socat=1.8.0.1-r0

WORKDIR /challenge

COPY . .

EXPOSE 1337

USER nobody

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 -u ./main.py,pty,stderr"]
