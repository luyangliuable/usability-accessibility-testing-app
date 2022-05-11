FROM trevinwadu/storydistiller-env

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 5037 5554 5555

WORKDIR /home

COPY . .

RUN chmod +x ./android-studio/bin/studio.sh

CMD ["./android-studio/bin/studio.sh"]
