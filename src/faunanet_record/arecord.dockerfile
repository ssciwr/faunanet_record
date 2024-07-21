FROM alpine:latest
ENV SAMPLE_RATE=44100
ENV CHANNELS=1
ENV DURATION=30
ENV FILETYPE=wav
ENV TYPE=S16_LE
# Use an absolute path
ENV OUTPUT_DIR=/root/faunanet/data
# ENV DEVICE=hw:0,0
ENV OUTPUT_PREFIX=alsa

RUN mkdir -p ${OUTPUT_DIR} && apk add --no-cache bash alsa-utils alsaconf

CMD mkdir -p ${OUTPUT_DIR}/${OUTPUT_PREFIX} && \
    arecord -f ${TYPE} -c ${CHANNELS} -r ${SAMPLE_RATE} -t ${FILETYPE} --use-strftime --max-file-time=${DURATION} ${OUTPUT_DIR}/${OUTPUT_PREFIX}/%F_%H:%M:%S.wav