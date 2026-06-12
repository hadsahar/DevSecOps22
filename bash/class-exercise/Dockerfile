FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
nano \
vim \
curl \
wget \
grep \
gawk \
coreutils \
procps \
tree \
man-db \
less \
zip \
unzip \
rsync \
openssh-client \
iputils-ping \
python3 \
python3-pip \
git \
python3.14-venv \
&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/marcusmueller/markmedown
RUN cd markmedown && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt


RUN useradd -ms /bin/bash student

WORKDIR /home/student

COPY generate_data.sh /home/student/generate_data.sh
COPY generate_exercises.sh /home/student/generate_exercises.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /home/student/generate_data.sh
RUN chmod +x /home/student/generate_exercises.sh
RUN chmod +x /entrypoint.sh

RUN chown -R student:student /home/student
USER student

ENTRYPOINT [ "/entrypoint.sh" ]