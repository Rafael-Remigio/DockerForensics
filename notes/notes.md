# Notes from the different pappers and Docker Documentation


# About Docker

## Docker vs VMs

The difference between the Containers and the Virtual
Machines lies in the underlying virtualization technology used
by them, which creates a major difference in their
performance. Containers share the host OS kernel, which leads
to the lack of isolation. Virtual machines, on the other hand, run in a
hypervisor environment where each VM is required to have its
own dedicated OS and other resources like related binaries,
libraries and application files. This not only consumes a
significant amount of system resources but also creates a huge
overhead, when multiple VMs are made to run on the same
physical server. A container takes just seconds to start while a VM
might take several minutes as startup time

<img src="images/docker-vs-VM.png">

### Docker Containers 

Tools like Docker make use of the container engines.
Here, containers act as portable means to encapsulate the
applications and their dependencies. As a result, managing
dependencies between containers in multi-tier applications
becomes quite a challenge. Containers isolate processes
from each other. A simple architecture of Docker container is
depicted in the Figure bellow. The core of Docker consists of Linux
Containers and LXC. LXC is a user-space control package
used for Linux Containers. It also provides components like
Control Groups (Cgroups). The main functionality of the
kernel-level namespaces provided by LXC is to provide
isolation between host and the container. Cgroups help Docker
to limit the consumption of resources by a container and they
also provide certain metrics to monitor the resource
consumption of the various processes within the containers.

<img src="images/docker-container-arch.png">

## Docker API
[Docker-API]

https://docs.docker.com/engine/api/v1.43/#tag/Container/operation/ContainerTop

<img src="images/docker-api-1.png">
<img src="images/docker-api-2.png">
<img src="images/docker-api-3.png">
<img src="images/docker-api-4.png">
<img src="images/docker-api-5.png">
<img src="images/docker-api-6.png">


Dumping process memory from docker container:
* https://stackoverflow.com/questions/75475032/dump-docker-container-memory
* https://www.reddit.com/r/docker/comments/rcgzru/get_docker_container_memory_dump_for_analysis/


## Docker File System Layers 

By default, all the changes made inside the container are
stored in the writable layer of the container built on the top of
the read only layer of images. This means that:
* Once the container is deleted, all the data inside the
container won’t persist.
* There is a tight coupling between the writable layer
of the container and the host machine due to which
the movement of data from one location to the other
would be difficult.
* In order to write something into a container's writable
layer, there would be a requirement of a storage
driver to manage the filesystem. By using data
volumes, we can write directly to the host filesystem.

To persist data, Docker has two options for storing files
on the host machine: volumes, and bind mounts.

For more info there is this video:

<iframe src="https://www.youtube.com/watch?v=Bc0iWolzaz4"></iframe>

<img src="images/docker-layers.jpg">

An image has many layers. When a container starts, only one read-write layer is attached on top of all the layers of images.

All the changes a container makes are made to the editable R/W layer and not to the underlying image layers. Therefore, a number of containers can use the same image with each having its own R/W layer.

Copy-on-Write (CoW) mechanism in its storage drivers. This mechanism satisfies the need of different containers to share the same image. However, when a single container performs operations such as modification of an image file, a duplicate image is created in the upper read-write layer.
Advantages of using Docker Layers

* Good storage management
* Faster builds
* Faster deployments
* Sharing across multiple containers
* Enhanced scalability

### Conclusion:

Docker Layers and Cache are important concepts when it comes to adopting good practices of creating any Docker infrastructure. Small tweaks here and there can increase the efficiency of scalability and deployments.

I have tried to explain the concepts in a simple and easy to understand language here to make readers interested into using these in their docker practices.

## Volumes

Volumes are managed by Docker and are the best
way to persist data. They are stored in a part of the
host file system. (/var/lib/docker/volumes/ on Linux). Non-Docker
processes are not allowed to modify this part of the
filesystem. Volume upon creation is stored within a
directory on the Docker host. On mounting the
volume to a container, this directory is what is
mounted into the container. Any given volume can be
mounted to multiple containers at the same time.
Even if no container is using a volume, it is still
available to use and is not deleted automatically

<img src="images/volumes.png">


## Four Basic Modes of Docker Network

https://community.pivotal.io/s/article/Explaining-Four-Basic-Modes-of-Docker-Network?language=en_US

* **Bridge Mode Networking**

    When docker daemon bootstrapped, a virtual bridge called docker0 will be created, and all the nic created in containers will connect to this bridge. It is working in layer2. IP address will be allocated in a subnet of docker0, and the gateway is docker0. Virtual nic pair will be created, in container side it is eth0, in host side it is vethxxx (naming like this), vethxxx will be added to docker0 bridge afterwards. If you use "docker run -p" to do port mapping, iptables rules will be created to do port mapping work between container and host.

    <img src="images/bridge.jpeg">


* **Host Mode Networking**

    When create and bootstrap container using host mode, this container will not have a unique network namespace, but share network namespace with the host. No virtual nic would be created and no IP address will be allocated. But filesystem, proc information is isolated from the host.

    <img src="images/host.jpeg">

* **Container Mode Networking**

    In this mode, the newly created container will share the same network namespace with an existing container. New container will not create its own nic and allocate new IP, it shares IP address and port with the existing container. And the same, except network, filesystem and proc information are isolated. This mod is very like Kubernetes' pod infrastructure.

    <img src="images/container-mode.jpeg">

* **None Mode**

    In this mode, docker container has its own network namespace, but no network configuration would be done for it, which means docker has no nic, IP address, routing information. We could add them once we are going to do it.

# Papers

## Insight from a Docker Container Introspection 

[TOOLS]
```
introspection tools, which are able to acquire data
from a system as it is running, can be utilized as both
an early warning system to protect that system and as
a data capture system that collects data that would be
valuable from a digital forensic perspective.

(...)

the data about containers must be accessed/collected
while they are executing. In order to access this data,
application programming interfaces (APIs) have been
created and leveraged to create introspection tools
[22, 23]. These introspection tools have the ability to
obtain data from a running container environment
regardless of running time.

[22] Prometheus - Monitoring system & time series
database. 2018.
[23] Datadog, Infrastructure & Application Monitoring as
a Service | Datadog. 2015
```

```
he research contribution of this paper is an
initial analysis of the viability of introspection tools
for performing a security analysis of containerized
software. 
```


[TOOLS][VMS]
```
Whereas previous approaches dealt with
hypervisors and/or underlying systems in cloud
infrastructure, Casalicchio and Percibali [38] focused
specifically on containers. In particular, they sought
to determine if tools collected the same information.
The researchers tested a battery of traditional Linux
metrics including iostat and mpstat as well as
utilizing the container specific cAdvisor [39] and the
platform specific docker stats command to pipe
metrics into both Prometheus [22] and Grafana [40]
for collection. Tests centered upon CPU and Disk I/O
intensive workloads. They determined different tools
present similar but not completely equal results.
```

[Docker-Swarm]
```
he previous studies concentrated on gathering
behavior and performance evidence of various types;
however, the scalability of the approaches was not
directly assessed. Stelly et al. [44] dealt with this
issue via the containerization of the digital forensics
process with their SCARF toolkit. They focused on
scalability across large platforms using Docker
Swarm, and attempted to prove that while the data
needed for forensic analysis continue to expand as
cloud adoption increased, their platform could extend
just as easily by showing high throughput. The group
ran tests on both a legacy cluster, and a cluster with
cutting edge hardware and found that several of the
components of the SCARF system, such as Yahoo’s
OpenNSFW network [45], had large throughput gains
comparing the two systems.
```

### Experiment

[Prometheus]
```
Prometheus is an open source introspection tool
that provides the ability to check multiple nodes in a
containerized architecture

Prometheus utilizes the
Docker API, which allows Prometheus to access data
via a well-defined data pipe; this also mitigates the
amount of stress on the system. In order to use the
service, ports have to be opened within the Docker
environment, as well as configured within
Prometheus to listen and scrape information from the
Docker environment
```

**Docker API** - in the papper they talk about how Prometheus uses the docker API. This API may be used to do forensics on containers during runtime. https://docs.docker.com/engine/api/v1.43/#tag/Container/operation/ContainerTop



## Forensic Analysis of Docker Swarm Cluster using Grr Rapid Response Framework


[Docker-usage]
```
Currently, Docker is one of the container ma-
chines implemented by almost 25% of the world’s Internet
companies [1,2]. Fig. 1 shows a significant rate of Docker
utilization in Internet companies until the beginning of 2018.

[1] D. Liu and L. Zhao, “The research and implementation of cloud com-
puting platform based on docker,” in Wavelet Active Media Technology
and Information Processing (ICCWAMTIP), 2014 11th International
Computer Conference on. IEEE, 2014, pp. 475–478.
[2] Datadog, “8 surprising facts about real docker adoption,”
https://www.datadoghq.com/docker-adoption/, 2018.
```

It's mostly about network analysis, and Grr Rapid Response Framework, not very usefull for this work.

## A Method of Docker Container Forensics Based on API


[Docker-API]
```
The paper explains Docker service principles and structural
features, and analyzing the model and method of forensics in
related cloud environment, then proposes a Docker container
forensics solution based on the Docker API. In this paper, Docker
APIs realize the derivation of the Docker container instances,
copying and back-up of the container data volume, extraction of
the key evidence data, such as container log information,
configuration information and image information, thus conducts
localized fixed forensics to volatile evidence and data in the
Docker service container. Combined with digital signatures and
digital encryption technology to achieve the integrity of the
original evidence data protection.
```


### At this stage, Docker container forensics mainly faces the following problems:

[Docker-Problems]
```
1) Evidence Volatility: The Docker container application service
is deployed on the cloud server. After the container is deleted, the
data in the container will also be deleted. And its virtualization
resources will be recycled, resulting in the complete loss of data
within the container, that is, the volatile data in the Docker
application service online will be lost and can’t be retrieved.
```
```
2) Evidence Integrity: The integrity of evidence needs to be
maintained during the current cloud forensic investigation, but this
is very difficult. Data integrity is a difficult part of the cloud
forensics process, the original data can’t be modified.
Additionally, Docker container forensics must be able to source
raw data from a running container based on the CSP without
affecting the service provided by the CSP, and because the host
that provides Docker application services may come from
different CSP, it is necessary to implement the authentication and
authorization of the forensics and the CSP
```
```
3) Cross-platform, cross-host container forensics. As a lightweight
virtualization technology, Docker is widely used to build PaaS
platform. But unlike IaaS, PaaS can run on multiple independent
hosts, even if the hosts come from different service providers.
This requires that container forensics not only take data from a
host's container, but also manage the forensics process on multiple
hosts.
```

### API-based Docker Container Forensics Program

This is very similar to what we wanna do.

[Docker-API]

**Analysis of the Docker Directory**
[Docker-Images]
```
1) The graph directory to store all the image's description file. For
each image layer, the graph directory has two files json and
layersize, and json file records the corresponding Docker image
ID, dependencies, create time and configuration information, etc.,
layersize records the size of the Docker image, and the complete
data of the image itself is stored in the/var/lib/docker/aufs/diff
directory.
```
[Docker-Container]
```
2) Containers stored in the container directory configuration
information, the configuration information contains all the
metadata of a container. As table 1 shows below:
```
Container configuration file and content

file name | file content
|---|---|
|\[container-id]-json.log | container log information|
|hostconfig.json | define the distribution of each resource
container|
| hostname | define the host name inside the container| 
| hosts | define the container's routing table |
| resolv.config | define the container's DNS server address|
| resolv.config.hash |the hash value of the resolv.config file|
[Docker-Volume]
```
3) The Docker data volume is a mechanism introduced for the
sharing and persistence of files and folders between containers
and hosts, between containers and containers. When creating a
volume from a folder in a container, the volume's ID directory is
included in the/var/lib/docker/volume path, which means any
changes in the container's mounted folder are reflected directly in
the host/var/lib/docker/[container-ID]/_data path, at the same time
this reflection is bidirectional.
```

**Docker API**

<img src="images/docker-api-6.png">

[Docker-API]
```
Using the related APIs, we can Program using docker-py
libraries from Docker's official portals for listing containers,
viewing information, running processes, getting logs, exporting
containers, generating container snapshots, copying directories /
files from containers, Such as container data, container log
information, container configuration information, and container
mounting data volume, etc. The system can obtain the information
of the object of the forensic object, such as container data,
container log information, container configuration information,
container mounted data volume, and the like
```

## INCIDENT ANALYSIS AND FORENSICS IN DOCKER ENVIRONMENTS

```
Previous forensic methods focus predominantly on physical or virtual machines, which do not
fundamentally differ in the actual analysis steps. However, it has not yet been considered how traditional
processes must be changed to assimilate the use of Docker containers. This article tries to contribute to
close this gap
```

As explained before, the read and write layer refered in the paper is the active filesystem inside the active container. An explanation and diagram can be found in the beginning of the papper.

### Difference from normal enviorments

Basicaly, just dumping the File System of the host and analyzing will not give us the full picture of the files inside the container

```
In principle, a forensic analysis gets started on a Docker host just like on a regular system: A dump of the
hard disk and ideally the main memory is created. However, the analysis of the dumps may provide
incomplete results, unless the specifics of (Docker) containers are taken into account. A typical analysis of
disk and memory dumps would still result in a list of files and processes, but the mapping to containers, or
even information about whether certain files are relevant for the reconstruction of the actual file system
view of the live system would not be included. The following sections represent various aspects to
consider, when analyzing Docker hosts to provide a comprehensive forensic analysis.
```

```
For example, searching for files on a disk dump of the host system will also find files from Docker Images.
However, the following additional questions must be answered on a Docker host:
1) Which image provided the given file?
2) Which containers used the given file?
3) Was the file deleted at container level? (This operation is potentially different from deletions on
regular file systems)
To answer these questions, it is relevant that an image can be used by several containers by using the r/w
layer. An association between files and containers is (only) possible via runtime information and, if
available, specific configuration files. 
```

```
If a runtime analysis is not possible, various
configuration files contain information about containers on the system. The default directory for Docker’s
configuration is /var/lib/docker. Container configuration is stored in
/var/lib/docker/container/ContainerID. Containers that are currently being executed can be
identified by two characteristics: On the one hand, the container configuration config.v2.json contains
the attribute Running: true and on the other hand, the Linux file system permissions of the container
subdirectory shm are set to 1777. There is also a dedicated directory for the r/w layer that indicates
whether a container has been started in the past (see Section 4.2.2)

Furthermore, it must be identified whether the file originates from a container (i.e. the r/w layer) or an
image. This information is relevant for analyzing the visibility of the file at runtime. If a file is deleted within
a container, there are two possibilities for the deletion:
1) The file originates from the r/w layer: In this case the file is deleted with normal operating system
mechanisms on the underlying file system layer.
2) The file originates from an image layer: In this case, a deletion reference is left in the r/w layer, but
the file remains present in the image layer.
Accordingly, different methods must be used to recover deleted files, which we explain in the following
sections
```

### Recovering files

Not specific to docker but files sometimes may be recoverable if the memory is analyzed. Out of the scope of the project but also possible. 

```
If a file which was stored in the r/w layer of the container is deleted, this file (reminder: which is stored as
a regular file in the host file system) is deleted in the file system of the host. Which metadata is retained in
the file system and how it can be recovered depends on the actual host file system (such as ext3, ext4, zfs,
...). It would be beyond the scope of this article to address the specificities, but these are not specific to
Docker, but common forensic file system analysis conditions and are well known and well documented
(Carrier, File System Forensic Analysis, 2005).

methods for recovering a deleted file from the r/w layer correspond to those
used in the forensic analysis of a physical disk or virtual disk
```

It differs a bit thought because the machine may not be analyzed from within itself

```
It should be noted that with a classic virtual machine, it is also possible to directly
analyze the hard disk device (such as /dev/sda) from within the virtual machine with forensic software. This option does not exist in Docker containers (even with root privileges)
because the device can not be opened
```

```
Basically, there are two common file recovery methods available:
1) File Carving
2) Filesystem Analysis
```


**File Carving**

Out of the scope of this project but it's kinda interesting and may be talked about in the report nontheless

```
typically used to describe the method of linearly
searching a volume, disk image, or file for characteristic patterns (magic bytes) for the beginning and/or
end of files. Since the file system is not considered, this approach can recover both allocated and deleted
files that have not yet been overwritten. However, fragmented files (with a few exceptions from specialized
carvers for certain single file types) can only be reconstructed incompletely. Furthermore, any meta-
information about the files, such as their filename, path, timestamp, or similar is missing.


the usage for forensic investigations in the Docker environment is subject to
problems: Assigning a previously deleted file recovered by file carving to a specific container, or even just
distinguishing whether the file belonged to a Docker container or the host system itself, is only possible
with metadata. However, as discussed above, files that have been restored by carving usually lack such
information, so that a reliable assignment is no longer possible. Only if the content of the file itself
provides information about its context (for example, if it contains a ContainerID), an association can be
made.
```

**file system analysis**

```
In contrast to file carving, the file system analysis uses management structures stored in the file system,
such as the MFT (master file table) in the case of NTFS or the inode tables of the group descriptors in the
case of ext file systems. Depending on the file system and circumstance, deleted files can also be
recovered based on this information, as described in detail by Brian Carrier (Carrier, The sleuth kit, 2007)
```

**Recovery of Files of an Image Layer**

```
In this case, a deletion reference is stored in the r/w layer as shown in Figure 3, but the file remains in the image layer.
Overlay2 allocates an inode in the r/w layer, which bears the name of the deleted file and is marked as a
character device by a file system flag. Thus, all files deleted in a lower layer can be identified by the
following command: find /var/lib/Docker/overlay2/$ContainerID/diff -type c. File recovery is
then possible by means of iterating through the layers and checking whether the corresponding file is
existent.
We would like to note that the procedure described here works analogously in the post-mortem analysis of
the entire host system. Equally, corresponding inodes can be identified and, if appropriate, the associated
files can be extracted from the directory of the underlying layer containing the original file
```

<img src="images/docker-deletion.png">


### Processes


```
The PIDs on the host are always unique, only the PID within the container can
be displayed identically to a PID on the host. This fact becomes relevant when log files contain PIDs and
should be used for post-mortem analysis. A translation from container PID to host PID is not possible
without runtime information.

Similarly to PID namespaces, user namespaces allow to map a user ID (UID) or group ID (GID) from one
container to another UID on the host. For example, a process can run inside a container with UID 0, but the
corresponding process on the host runs with UID 65000. Like in PID namespaces, this results in problems
in the analysis if log files contain UIDs, but in this case an assignment of container UID/GID to host
UID/GID via the /etc/subuid and /etc/subgid is possible.
```

### Summary

```
we discussed the possibilities, difficulties, and
approaches for the reconstruction of deleted files and their association with Docker containers, notably
the differences in the layer from which a file was deleted (Section 4.2 and 4.3), and the differences in the
assignment between AUFS and Overlay2. We also discussed the possibilities and limitations of file
recovery with file carving. dealt with forensically relevant aspects of Docker namespaces, while
Section 4.5 dealt with the so-called cgroups and the topic of container management
```

### Script provided

```
#!/usr/bin/env bash
set -e
if [ -e $1 ];
then
    echo "Please provide container ID as argument."
    exit
fi


short_id="$1"
docker_lib="/var/lib/Docker"
docker_containers="$docker_lib/containers"
docker_overlay="$docker_lib/overlay2"

tmp_dir=$(echo $docker_containers/$short_id*)

if [ ! -d $tmp_dir ];
then
    echo "No container matched the provided container ID."
    exit
fi

long_id=$(basename $tmp_dir)

image_id=$(grep -Po ’Image":.*?[ˆ\\]",’ \
    $docker_containers/$long_id/config.v2.json | \
    grep sha256 | cut -d ":" -f "3" | cut -d ’"’ -f 1)

image=$(grep -Po ’Image":.*?[ˆ\\]",’ \
    $docker_containers/$long_id/config.v2.json | \
    grep -v sha256 | cut -d ’"’ -f "3")

mount_id=$(cat $docker_lib/image/overlay2/layerdb/mounts/$long_id/mount-id)
path_to_rw_layer="$docker_overlay/$mount_id/diff"
path_to_live_mount="$docker_overlay/$mount_id/merge"
# list is ordered from highest layer to lowest layer
layer_list=$(cat $docker_overlay/$mount_id/lower)

IFS=’:’ read -r -a layer_array <<< "$layer_list"
echo "=========== Container $long_id ======================="
echo "|"
echo "| Image:
$image"
echo "| ImageID:
$image_id"
echo "| MountID:
$mount_id"
echo "| Container Config: $docker_containers/$long_id"
echo "|"
echo "|====================================================="
echo "| Layers:"


for index in "${!layer_array[@]}"; do
    if [ $index -eq 0 ];
    then
        continue
    fi
    ll=$(readlink $docker_overlay/${layer_array[$index]})
    layer=$(echo $ll | cut -d ’/’ -f 2)
    echo "| $docker_overlay/$layer"
    echo "|------------------------------------------------"

done
```

## Security Analysis and Threats Detection Techniques on Docker Container

```
Theo et al.
proposed the notion of ecosystem security for Docker
container and argues that the security of third-party modules
and security in the Docker development lifecycle should be
strengthened [14]. Yet, no detailed solution is proposed. The
mainstream Docker scanning tools include Clair,
DockerScan, Anchore and so forth. However, they mainly
focus on the static security, i.e. only focus on the threats on
Docker images, but cannot provide the dynamic monitoring
for the running Docker container instances. Moreover, P.
Salvatore et al. mentioned that Docker monitoring needs to
consider the updating problems of Docker container, which
means the monitor system has to keep pace with the rapid
changing Docker container’s life-cycle [15].
```

```
Compared to the existing work on Docker security, this
work has the following novelties.
* We make a detailed analysis on the existing
mechanisms inside Docker container technology and
thoroughly discuss the threats for Docker container
from various aspects.
* Apart from theoretical analysis for Docker container,
we propose a comprehensive threats detection
framework for Docker container and conduct a
detailed experiment which proves the effectiveness
of this framework.
* The proposed detection framework can not only
recognize the risks form static Docker image by
scanning malicious files and vulnerabilities, but also
promise the security of the dynamic Docker
container instance by monitoring the DoS risks and
dangerous IP/DNS requests.
* By introducing the machine learning techniques, we
can predict the unknown threats which are not
recorded in some threat intelligence databases like
common vulnerabilities and exposures (CVE) or
blacklists of malicious domain
```

### EXISTING SECURITY MECHANISMS FOR DOCKER CONTAINERS

```
Docker container does not isolate the virtual objects via
virtualizing hardware or using an independent operating
system. Rather, it uses the Namespace mechanism in Linux
to promise the secure isolation of running environments and
uses the Cgroup mechanism in Linux to realize the
management of computer resources. Moreover, it utilizes the
kernel capability to reinforce the security [16
```

```
Isolated containers
cannot access the resource from other containers and thus
promises the transparency of computer resource access [17].
By Namespace, each container instance can have its own
complete network, file system, IPC (Inner-Process
Communication
```

### THREATS ANALYSIS FOR DOCKER CONTAINER

* Components Security
* Container Escape Attack
* Sensitive Information Leakage
* Network Mode Security

### DOCKER THREATS DETECTION FRAMEWORK


```
The detection considers
two aspects of security: docker image security and container
instance security. For docker image, we detect the
vulnerabilities and exposures of pre-installed applications by
CVE (Common Vulnerabilities & Exposures) database and
use malicious signature database to achieve the goal of
finding out malicious files. Yet, these two detections can
only find the known threats which are stored in the public
databases. Hence, we introduce a malicious predicting
module based on machine learning algorithm, which can
predict the potential malicious files and thus prevent the
unknown attacks. For running container instance, we monitor
two aspects: computer resource usage and IP/DNS requests
```

Good article, not very usefull for our porpuse of forensics post mortum. Good for the report as a reference maybe


## Evaluation of File Carving Tools for Forensic Investigation in Docker Containers

###  BACKGROUND
This section aims to provide detailed background knowledge
of various concepts involved in this paper.

### File carving
```
after a file is deleted, only the pointer pointing to the
location of the files on the disk is removed. The storage space
at which the data of the deleted file is located is now available
for new data to be stored. As long as this new data has not
been overwritten over that space, the contents of the deleted
file can be recovered via certain forensic technique

There are many File Carving Tools available in the market
for Linux. Some of the popular ones are: PhotoRec, Scalpel,
Foremost, Bulk Extractor with Record Carving and TestDisk
```
### Results
```
From the experiments conducted, we can conclude that the
container forensic investigation does not differ much from an
ordinary forensic investigation on a host machine. The same
tools can be used to successfully extract data from containers
as well. File carving attempts to recover deleted files. This,
however, does not always succeed and is dependent on
multiple factors. The overall good success rate of the file
carving performed in our experiments indicates that it can be a
viable and effective method of extracting data from removed
containers. All the file carving tools used in the experiments
got almost similar performances for certain file types (jpg and
pdf). None of the tools were able to recover the docx file type.
However, overall the performance of Scalpel and Foremost
comes out to be better as compared to the Photorec in our
experiments
```

I don't thing file carving will be implemented but it is good to know that it does not differ from simillar recovery techniques on Linux Machines.


# Online article and Posts

## hacktricks

### Container modification

Find the modifications done to this container with regards to the image with:

```
docker diff wordpress
C /var
C /var/lib
C /var/lib/mysql
A /var/lib/mysql/ib_logfile0
A /var/lib/mysql/ib_logfile1
A /var/lib/mysql/ibdata1
A /var/lib/mysql/mysql
A /var/lib/mysql/mysql/time_zone_leap_second.MYI
A /var/lib/mysql/mysql/general_log.CSV
```

In the previous command C means Changed and A, Added.
If you find that some interesting file like /etc/shadow was modified you can download it from the container to check for malicious activity with:

```
docker cp wordpress:/etc/shadow.
```

Compare it with the original one running a new container and extracting the file from it:

docker run -d lamp-wordpress
docker cp b5d53e8b468e:/etc/shadow original_shadow #Get the file from the newly created container
diff original_shadow shadow


### Image modifications

When you are given an exported docker image (probably in .tar format) you can use [container-diff](https://github.com/GoogleContainerTools/container-diff/releases) to extract a summary of the modifications.


### Basic Analysis

You can get basic information from the image running:

```
docker inspect <image> 
```

You can also get a summary history of changes with:
```
docker history --no-trunc <image>
```

### Credentials from memory

Note that when you run a docker container inside a host you can see the processes running on the container from the host just running ps -ef

Therefore (as root) you can dump the memory of the processes from the host and search for credentials
https://book.hacktricks.xyz/linux-hardening/privilege-escalation#process-memory7


## compass-security

### Wrong Assumptions

```
At first, I made some wrong assumptions about docker persistence. I though only the Volumes and Bind Mounts you add are kept when containers are stopped. This is not correct.

As soon as a Docker Image is converted to a Container (docker run), a Union Filesystem is created in the according subdirectory in /var/lib/docker . Any data the Container read and writes is stored in this filesystem. If you stop a Container the data is still there and you can start the Container again and continue where you left off. Also the log file in /var/lib/docker/containers/YOURCONTAINERID/YOURCONTAINERID.log is persistent.

However, if you delete the container (docker rm) you loose all persistent data except the Volumes and Bind Mounts. Unfortunately this is was happened on the analyzed system and a lot of potentially interesting data was gone.
```

### Volumes / Mount Binds / Tmpfs

```
Union filesystem provides persistence, its not the recommended way to persist data because if you delete a Container, the data is gone. Docker recommends to use Volumes and Mount Binds to persist data that is required to stay alive longer than the Container.

Volumes in the end are again just folders inside of /var/lib/docker/volumes

Mount Binds on the other hand are like soft links to the host file system whereas tmpfs only is in memory, therefore data is lost after the Container is stopped.
```

### Data

```
All data inside the Containers is available transparently to the host. It is mostly just scattered in those layer folders in /var/lib/docker

It seemed that the used Docker orchestrator software, forwarded the NGINX Docker logs to the syslog of the host. This was extremely valuable, as all potential dangerous requests to all applications where recorded.
```

Very cool story not very usefull for this project

## sysdig

### Container Forensics Techniques

There are various tools and techniques available for conducting container forensics. Some of the most commonly used tools and techniques include:

* Image analysis: Analyzing container images to identify vulnerabilities, configuration issues, and other potential security threats.
* Log analysis: Analyzing log files to identify suspicious activity, such as unexpected network connections or changes in resource utilization.
* File system analysis: Analyzing the file system of a container to identify malicious files or modifications.
* Memory analysis: Analyzing the memory of a container to identify malicious activity, such as malware infections.
* Network analysis: Analyzing network traffic to identify potential security incidents, such as data breaches or malware infections.

Docker includes tools for forensic analysis, such as the Docker CLI’s commands for accessing container metadata and the Docker API’s access to metadata and logs


## cado security

Preservation & Investigation

In the event an incident occurs, it is critical to preserve the evidence that’s required to allow for an in-depth investigation:

* Never destroy the node when compromised! This will make it impossible to identify root cause
* Determine which evidence you plan to capture and ensure its enough visibility to determine root cause and impact — remember, the more data sources you can analyze, the better your investigation will be
* Have a plan for how to capture the data you need and test your ability to capture it- given the dynamic and ephemeral nature of containers, automation is key
* Know how to snapshot the host that contains the containerized disks


## Red Hat blog - Docker Forensics for Containers: How to Conduct Investigations

Containers make digital forensics incredibly complex, as they are scheduled and orchestrated across different hosts according to usage and need. Furthermore, container environments yield enormous amounts of data at high velocity, which is difficult to capture without the right type of instrumentation and tools.

Containers differ from bare metal or virtual machines in a number of ways that impact obtaining actionable evidence. At this time there is no default “container snapshot” function available; containers must be captured as a set of distinct components.

### File System

Leading container runtimes use a copy-on-write file system. This is a great advantage to forensic acquisition. All of the default system and application files exist within the container image. Any changes since the container started are stored in a separate directory from the original image. Furthermore, any deletion of original files from the image is also recorded.

But we can go one step further: Docker will capture all file modifications, since the container was started into a new layer on the copy-on-write file system. Simply commit an existing container, running or not, into a new image: ```docker commit $CONTAINER_ID imagename```. Committing a container into a new image does not otherwise modify the container in any way. Note that committing a container differs from snapshotting a VM. Committing only records file system changes, but not the current process execution state.

### MEMORY

Processes running inside a container manage memory the same as any other process. By default, processes inside a container may not interact or interfere with memory controlled by any process outside the container. This provides the following characteristic: if you capture all of the memory for each process in a container, you have captured all allocated memory for that container.

There exist multiple per-process memory dump utilities in linux. The utility
gcore suspends the process during acquisition but does not modify it; it executes it quickly, and the output format is compatible with YARA.

### Shared Volumes

Containers are ephemeral. Malware might not be aware of this and write some interesting data to the container’s allocated disk space. Ultimately the most sensitive data is likely stored via a volume

Identifying the volume mount is simple; one inspects the container. Volumes are identified via the Volume and Mount configuration. Existing examination techniques will be needed for each backing service.

### Container escape

There are vulnerabilities and misconfigurations that could allow malware to escape a container. If there is any evidence of suspicious behavior on the host itself, or evidence of this type of malware, it is prudent to image the entire host, whether bare-metal or VM.

A container may not be fully isolated in some cases, but until there is evidence of an
isolation bypass, one may assume that the suspicious behavior is constrained to the container’s environment.

Basically it's very hard to leave a container unless there are some serius misconfiguration.

To configure isolation in a secure way we need:


### Containers in a forensic environment

There isn’t a formal mechanism for running a captured container. Once they’re shut down, even if both file
system and memory contents are exported, there is no mechanism for combining the two back into the previous running state. Containers are designed to be ephemeral and allocate new memory on startup.

For forensics it is better to have the container running. If the container needs to be isolated there are two possibilities:

* First, containers may be paused at any time. Container execution is completely suspended, memory remains allocated, volumes remain mounted, etc. Any malware currently executing is interrupted.
* Second, containers may be quarantined by removing network access or system call privileges. The container processes – and possibly the malware – will continue to execute, but will be unable to send, receive, read, or write any data, or even unmap existing memory



## EFORENSICS: Digital Forensics in Docker Environments: Challenges and Solutions

By understanding these challenges and implementing appropriate solutions, forensic investigators can effectively analyze Docker containers and preserve crucial evidence. 

### Isolation and Containerization Challenges 

Docker containers are designed to be self-contained and isolated from the host system and other containers. beneficial for security and performance but it poses challenges when it comes to forensic analysis. 

### Volatility and Transience of Containers 

Docker containers are inherently volatile and transient, with the ability to be created, destroyed, and re-created easily.

Traditional forensic approaches may not be suitable for dynamic Docker environments. Investigators need to adapt their techniques to capture and analyze data from running containers, considering the frequent creation and deletion of containers.

### Distributed and Orchestration Challenges

In distributed Docker environments, containers can be spread across multiple hosts, making evidence collection and analysis more challenging. 

container orchestration systems and the associated metadata becomes crucial for understanding the context and relationships between containers.

Basically the issue is that it's not just one highly volitile machine, it's possibly many, spread sometimes across multiple machines.

### Encryption and Secure Communication 

Communication between docker components is often encrypted as if it were differente machine even on the same enviorment. Encryption may hinder investigators' ability to access and analyze container communications,

### Forensics artifacts

In Docker environments, the traditional approach to identifying and preserving forensic artifacts needs adaptation. Investigators must familiarize themselves with Docker-specific artifacts such as container images, layers, volumes, and network configurations.

### Dynamic Network and IP Addressing

Docker containers can have dynamically assigned IP addresses and network configurations, making it difficult for investigators to track and analyze network communications. Traditional network forensic techniques that rely on static IP addresses and network flow analysis may not be applicable in this dynamic environment. 

<img src="images/docker-network.png">

### Solutions

*leveraging Docker's logging capabilities and system auditing features can provide valuable insights for forensic analysis.

* specialized forensic tools and techniques designed for Docker environments can assist in acquiring and analyzing containerized data


## EForensics - Security Assessment Tools for Docker Containers

Docker containers are attractive target for attackers or a potential hiding place for bad actors planning malicious activities. Docker forensics involves understanding the internal workings of containers, their file systems, network configurations, and runtime artifacts to uncover valuable evidence during an investigation.

### Challenges in Docker Forensics

* Containers can be created, modified, and destroyed rapidly, potentially leading to
the loss of critical evidence, which is often the case.
* Secondly, the layered
architecture of Docker images adds complexity to the forensic process, as each
layer may introduce additional artifacts or hidden data, such as slack space or the
lack of. 
* Thirdly, the distributed nature of container environments, such as container
orchestration platforms like Kubernetes, further complicates the forensic analysis
by involving multiple hosts and interconnected components.

### Techniques and Tools for Docker Forensics

* Firstly, the collection and preservation of Docker artifacts are paramount. These
include Docker images, container metadata, logs, and configuration files.
Techniques like live acquisition, memory forensics, or disk imaging can be
employed to capture container states and related data for analysis. 
* Tools such as Docker Bench, Docker Security Scanning, or Trivy can help identify vulnerabilities
or misconfigurations that might have been or able to be exploited for nefarious
purposes.
* Other specialized tools like RegRipper (https://github.com/keydet89/RegRipper3.0,n.d.), or Autopsy (https://www.sleuthkit.org/autopsy/, n.d.) can be used to parse the
container file system and extract relevant artifacts, such as logs, configuration
files, or user account information
* network analysis tools like Wireshark can be employed to inspect network traffic generated by Docker
containers, revealing potential communication with external entities or suspicious
patterns
* Memory forensics also plays a crucial role in traditional digital investigations. Tools
like Volatility, which is not covered within the scope of this article, can be applied
to extract the target information for analysis. However, conducting memory
analysis in Docker containers introduces some additional challenges

### DockerBench

Docker Bench is an open-source security auditing tool designed to assess the
security configuration of Docker containers and host systems

is widely used to evaluate Docker deployments against recommended
best practices and security benchmarks


### Trivy
Trivy is also an open-source vulnerability scanner specifically designed for
containerized environments.

Trivy can also analyze a local file system with a simple
command, “trivy fs.” Forensically speaking, this is super helpful and makes Trivy a
great tool not just for docker containers.


## EForensics - Forensic Investigation in Docker Environments: Unraveling the Secrets of Containers

Unlike traditional virtual machines, Docker containers do not
have a complete operating system, which makes evidence collection and forensics
difficult. Furthermore, the dynamics of containers, such as rapid creation,
modification, and destruction, add to the complexity of investigations.

### Challenges

* Evidence Gathering: The transient nature of Docker containers makes evidence
gathering a challenge. It is crucial to correctly identify and preserve relevant
artifacts, such as container images, metadata, logs and associated file systems.
* Data analysis: The lack of a complete operating system in Docker containers
requires different forensic approaches. Data analysis must take into account the
particularities of layered file systems, the interaction between containers, and the
isolation techniques used.
* Event reconstruction: The rapid creation and destruction of containers makes it
difficult to accurately reconstruct events. It is necessary to track and correlate
information dispersed in different containers and in distributed logs.

### Techniques

* Gathering evidence in Docker environments involves
identifying and preserving relevant images, containers, volumes, networks, and
metadata. This can be done through tools like the Docker CLI, Docker API, and
image registries.
* Data analysis: Forensics on Docker containers requires understanding layered file
systems and extracting key information. Tools such as DFF (Docker Forensic
Framework) and Autopsy can help analyze Docker containers.

### Network

<img src="images/docker-networks-diagram.png">


Network Complexity: Docker has a complex set of networking features that can
be challenging to configure and debug, especially in distributed environments.
Setting up advanced networks like load balancers or multi-host networks can be
tricky.


### Collecting evidence

specialized tools, such as the Docker Forensics Toolkit, to gather information
about running containers.

This command displays a detailed list of all running containers, including
information such as ID, name, image, status, exposed port, and more.

```docker-forensics container list```

```docker-forensics containers info <ID of the container>```

```docker-forensics images list```

```docker-forensics images info <ID of the container>```

```docker-forensics networks list```

```docker-forensics volumes list```

```docker-forensics container inspect <ID of the container>```

```docker-forensics container logs <ID of the container>```

```docker-forensics memory dump <ID of the container>```

```docker-forensics diff <ID of the container>```

### acquisition of container images for further analysis.

1. Copy Image to Acquisition Directory: Copy the container image to the acquisition directory mounted on the temporary container.
2. Remove temporary container: Remove the temporary container created for acquisition.

### Exploring Docker logs and event logs to reconstruct suspicious activity.

1. Identify the target container: Use the docker logs command to access the target
container's logs.
2. Explore specific logs: Use additional docker logs command options to explore
specific logs, such as filtering by date or searching by keyword.
    ```docker logs --since <initial_date> --until <final_date> <ID or container name>```
3. export the logs and use other tools to analyze them
    ```docker logs <id> > logs.txt```

### Extraction of metadata and configuration information from containers.

```docker inspect <id>```

Metadata example:
* Container ID
* Container name
* Image used
* Environment Variables
* Mounted directories
* Exposed doors
* Associated networks

### Access the container shell

```docker exec -it <contianer name or id> /bin/bash```

### Run a container for network analysis:

Within the network analysis container, use tools like Wireshark to capture and analyze network traffic.


### Container memory access

1. run an interactive session inside the container:
    ```docker exec -it <container name or ir> /bin/bash```
2. run volatility from inside the container. Profile should be the containers OS, usually ubunto or alpine
    ```volatility -f /proc/kcore --profile=<profile> pslist
3. on host, extract the dump
    ```docker exec <container name> cat /proc/kcore > memory_dump




## Dump memory from container from host

https://www.reddit.com/r/docker/comments/rcgzru/get_docker_container_memory_dump_for_analysis/


Saw this is stackoverflow.
```
I used GNU Debugger or gdb for generating the core sump for a container from outside the container,

    "sudo docker ps -a | grep service_container_name" to get the container id.
    "sudo docker inspect [container id] | more" to get the parent PID

    docker inspect -f '{{.State.Pid}}' <CONTAINER ID> #to get the parent PID
    pstree -pg [parent pids] # to get the child PID
    sudo gcore PID # dump memory with gcore
```



## CRIU

Checkpoint/Restore In Userspace, or CRIU (pronounced kree-oo, IPA: /krɪʊ/, Russian: криу), is a Linux software. It can freeze a running container (or an individual application) and checkpoint its state to disk. The data saved can be used to restore the application and run it exactly as it was during the time of the freeze. Using this functionality, application or container live migration, snapshots, remote debugging, and many other things are now possible.

CRIU started as a project of Virtuozzo, and grew with the tremendous help from the community. It is currently used by (integrated into) OpenVZ, LXC/LXD, Docker, Podman, and other software, and packaged for many Linux distributions. 

https://github.com/checkpoint-restore/criu

## Docker Statistics - CPU, MEMORY, I/O NETWORK, READ/WRITE DISK

https://www.docker.com/blog/how-to-monitor-container-memory-and-cpu-usage-in-docker-desktop/

```docker stats```




Container networking refers to the ability for containers to connect to and communicate with each other, or to non-Docker workloads.
A container has no information about what kind of network it's attached to, or whether their peers are also Docker workloads or not. A container only sees a network interface with an IP address, a gateway, a routing table, DNS services, and other networking details. 

Docker's networking subsystem is pluggable, using drivers/modes. Several drivers exist by default, and provide core networking functionality:

Bridge/Default Mode Networking: Bridge networks are commonly used when your application runs in a container that needs to communicate with other containers on the same ho

host: Remove network isolation between the container and the Docker host, and use the host's networking directly

overlay: Overlay networks connect multiple Docker daemons together and enable Used for docker swarms

Vlans: Macvlan networks are best when you are migrating from a VM setup or need your containers to look like physical hosts on your network, each with a unique MAC address.
IPvlan is similar to Macvlan, but doesn't assign unique MAC addresses to containers. Consider using IPvlan when there's a restriction on the number of MAC addresses that can be assigned to a network interface or port.

none Completely isolate a container from the host and other containers