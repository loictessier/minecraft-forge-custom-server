FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /minecraft

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O forge-1.20.1-47.4.0-installer.jar https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.0/forge-1.20.1-47.4.0-installer.jar \
    && java -jar forge-1.20.1-47.4.0-installer.jar --installServer

RUN echo "eula=true" > eula.txt \
    && echo "-Xms3G\n-Xmx6G" > user_jvm_args.txt

RUN chmod +x run.sh

EXPOSE 25565

ENTRYPOINT [ "./run.sh" ]

CMD [ "nogui" ]
