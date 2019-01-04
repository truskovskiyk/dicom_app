FROM qiicr/docker-dcmtk-cli

WORKDIR /app
EXPOSE 8083
COPY storescp.cfg storescp.cfg
CMD dcmrecv  --verbose 8083 --config-file storescp.cfg  default