FROM python:3-alpine

RUN apk update && apk --no-cache add git

COPY entry.sh /
RUN chmod +x /entry.sh

CMD /entry.sh
# CMD /bin/sh
