# DICOM records
This is WIP applications


## Test
TODO

## Local development
TODO

## Deploy [manual so far]
We use [kubernetes in GCE](https://kubernetes.io/docs/setup/turnkey/gce/) for a deploy
You will need 3 components for the deploy


### NFS server

1. Create persistent disk
```bash
gcloud compute disks create --size=10GiB --zone=us-central1-a dicmo-app-storage
```

2. Deploy NFS to k8n
```bash
kubectl apply -f ./deployment/nfs/nfs-deployment.yaml
kubectl apply -f ./deployment/nfs/nfs-service.yaml
```

3. Get NFS ClusterIP
```bash
kubectl get service nfs-server
```


### DICOM storage SCP (receiver)

[more info here](https://support.dcmtk.org/docs/dcmrecv.html)

1. Build docker images for dcmrecv

```bash
cd ./dcmrecv/
docker build -t dcmrecv .
docker tag dcmrecv:latest truskovskyi/dcmrecv:latest
docker push truskovskyi/dcmrecv:latest
cd ./../
```

2. Deploy
```bash
kubectl create -f ./deployment/dcmrecv/dcmrecv-deployment.yaml
kubectl expose deployment dcmrecv --type=LoadBalancer --name=dcmrecv-service
```

3. Get DICOM storage SCP IP
```bash
kubectl get service dcmrecv-service
```

4. Clean it
```bash
kubectl delete service dcmrecv-service
kubectl delete  deployments dcmrecv
```

### DICOM API

1. Build docker images for DICOM API
```bash
docker build -t dcmrecv_api .
docker tag dcmrecv_api:latest truskovskyi/dcmrecv_api:latest
docker push truskovskyi/dcmrecv_api:latest
```

2. Deploy
```bash
kubectl create -f ./deployment/dicom_api/dicom-api-deployment.yaml
kubectl expose deployment dicom-api --type=LoadBalancer --name=dicom-api-service
```

3. Get DICOM API
```bash
kubectl get service dicom-api-service
```

4. Clean it
```bash
kubectl delete service dicom-api-service
kubectl delete  deployments dicom-api
```

### Manual testing

1. Install [dcmtk](https://dicom.offis.de/dcmtk.php.en)

```bash
brew install dcmtk
```

2. Send test image
```bash
dcmsend --verbose <host> <port> <image>
example: dcmsend --verbose 35.239.174.149 8083 ./data/patient_1/image_49.dcm
```



## Plan

- [x] NFS server
- [x] DICOM storage SCP (receiver)
- [x] DICOM API
- [x] Manual Deploy
- [ ] Tests
- [ ] CI Deploy
