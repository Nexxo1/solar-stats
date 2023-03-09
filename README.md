# solar-stats

To Build

docker build --network=host -t solar-stats .

To Run

version: "3"

services:
  solar-stats:
    image: solar-stats:latest
    container_name: solar-stats
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Australia/Adelaide
        #      - RUN_OPTS=<run options here> #optional
    # volumes:
    #   - ./metrics.yaml:/config.yml
    # command:
    #   - --config.file=/config.yml
    ports:
      - "9877:9877/tcp"

    restart: unless-stopped
