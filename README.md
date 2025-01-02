# AIN3003 Option 1 Term Project

![image](https://github.com/user-attachments/assets/f9c34c95-65fc-4fcf-85ce-9be02713ecfe)



Hi, I chose the first option of the AIN3003 term project. The project's details and objectives are written below:



## Assignment

Using MongoDB on Kubernetes to Build and Launch a Containerized Python Applicationwith Flask,The purpose of this assignment is to develop a Python application that is scalable and containerized, capable of interacting with a MongoDB database, Flask, and to install it on a Kubernetes cluster.Students will gain important experience working with database interactions, Kubernetes orchestration, and containerization in a real-world setting with this project. It goes over the basic ideas behind setting up and running containerized apps in a distributed setting.

## Step 1

I've chosen minikube for the intention of using clusters. I've already had MongoDB and Docker installed on my device.
The first thing we need to do is starting our minikube service.

```bash
minikube start
```

## Step 2

After starting minikube, we need to create a Statefulset file in order to run a reliable and scalable database in a containerized environment. Secondly, we need a service.yaml file too. So that our MongoDB pods can be accesible internally and externally.

```bash
kubectl apply -f mongo-statefulset.yaml
kubectl apply -f mongo-service.yaml

```
After waiting some time for MongoDB pod to be ready, here's what our projects status look like:

```bash
NAME                             READY   STATUS             RESTARTS      AGE
pod/mongodb-0                    1/1     Running            1 (30m ago)   4d1h

NAME                      TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)     AGE
service/kubernetes        ClusterIP   10.96.0.1    <none>        443/TCP     6d1h
service/mongodb-service   ClusterIP   None         <none>        27017/TCP   4d1h

NAME                       READY   AGE
statefulset.apps/mongodb   1/1     4d1h

```

## Step 3
Now that our MongoDB deployment is ready, we need to import our data to the deployment:

```bash
C:\DEVEL\stage\var\resources>kubectl exec -it mongodb-0 -- mongoimport --host localhost --port 27017 --username admin --password admin --authenticationDatabase admin --db BOOKSTORE --collection bookstore --file /tmp/data.json --jsonArray
2024-12-29T19:31:10.171+0000    connected to: mongodb://localhost:27017/
2024-12-29T19:31:10.187+0000    9 document(s) imported successfully. 0 document(s) failed to import.

```
Now that we completely finished the MongoDB part, our focus shifts towards the Flask phase of this project.

## Step 4
In order to deploy a Flask app, we need to create our file. On default, our container's image is getting pulled off of Kubernetes with the latest version updating itself time to time. However, in order to have a stabilized app, the image will be pulled off of my docker hub repository. Also, for the app's API some .html templates have been created in order to perform CRUD operations.

```bash
kubectl apply -f flask-app-deployment.yaml
```
```bash
kubectl get all
```
```bash
C:\bookstoreapp>kubectl get all
NAME                             READY   STATUS    RESTARTS      AGE
pod/flask-app-864cf45dc5-5pww5   1/1     Running   0             3m27s
pod/mongodb-0                    1/1     Running   1 (72m ago)   5m1s

NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/kubernetes          ClusterIP   10.96.0.1      <none>        443/TCP          6m2s
service/mongodb-service     ClusterIP   None           <none>        27017/TCP        4m

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/flask-app   1/1     1            1           1m

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/flask-app-864cf45dc5   1         1         1       1m

```
## Step 5

Now we need to create a flask service:

```bash
kubectl apply -f flask-app-service.yaml
```
```
C:\bookstoreapp>kubectl get services
NAME                TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
flask-app-service   LoadBalancer   10.106.229.178   <pending>     5000:30936/TCP   8m16s
kubernetes          ClusterIP      10.96.0.1        <none>        443/TCP         7m34s
mongodb-service     ClusterIP      None             <none>        27017/TCP       8m7s
```
## Final Step
We are ready to service our project. You can freely inspect and experiment with the API.
```bash
minikube service flask-app-service
```

