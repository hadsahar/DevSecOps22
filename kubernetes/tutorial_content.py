"""All page content: cover, TOC, and every chapter."""
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (Paragraph, Spacer, PageBreak, Table,
                                  TableStyle, HRFlowable)
from reportlab.platypus.flowables import Flowable
from tutorial_draw import (ChapterHeader, CodeBlock, DiagramF, make_styles,
                            d_hierarchy, d_pod_lifecycle, d_rolling,
                            d_statefulset, d_daemonset, d_job, d_hpa, d_resources,
                            BLU, DRK, TEL, GRN, ORG, RED, GRY, MID, BOX, WHT,
                            colors, W, H, cm)

S = make_styles()

_ts = lambda extra=[]: TableStyle([
    ('BACKGROUND',  (0,0),(-1,0), BLU),
    ('TEXTCOLOR',   (0,0),(-1,0), WHT),
    ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTNAME',    (0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',    (0,0),(-1,-1), 9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor("#E8F4FD"), WHT]),
    ('GRID',        (0,0),(-1,-1), 0.5, BOX),
    ('TOPPADDING',  (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('VALIGN',      (0,0),(-1,-1),'MIDDLE'),
] + extra)


def cover(story):
    story.append(Spacer(1,1.5*cm))
    class Banner(Flowable):
        def __init__(self): super().__init__(); self.width=W-4*cm; self.height=8*cm
        def draw(self):
            w,h=self.width,self.height
            self.canv.setFillColor(BLU); self.canv.roundRect(0,0,w,h,16,fill=1,stroke=0)
            for cx,cy,r,a in [(w-60,h-40,80,.12),(w-20,20,50,.08),(40,h-30,60,.08)]:
                self.canv.setFillColor(colors.Color(1,1,1,a)); self.canv.circle(cx,cy,r,fill=1,stroke=0)
            self.canv.setFillColor(WHT); self.canv.setFont('Helvetica-Bold',30)
            self.canv.drawCentredString(w/2,h-58,"Kubernetes Workloads")
            self.canv.setFont('Helvetica-Bold',17)
            self.canv.setFillColor(colors.HexColor("#BDD7FF"))
            self.canv.drawCentredString(w/2,h-85,"A Complete Teacher's Guide with Diagrams & Examples")
            self.canv.setFillColor(WHT); self.canv.setFont('Helvetica',11)
            self.canv.drawCentredString(w/2,h-112,"Pods · ReplicaSets · Deployments · StatefulSets · DaemonSets · Jobs · HPA")
    story.append(Banner()); story.append(Spacer(1,.5*cm))
    meta=[["Topic","Kubernetes Workload Resources"],["Audience","DevOps Students (Intermediate)"],
          ["Duration","3–4 classroom hours"],["Version","Kubernetes 1.29+"]]
    t=Table(meta,colWidths=[4*cm,10*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor("#E8F4FD")),
        ('TEXTCOLOR',(0,0),(0,-1),BLU),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),
        ('FONTNAME',(1,0),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),10),
        ('GRID',(0,0),(-1,-1),.5,BOX),('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.HexColor("#E8F4FD"),WHT]),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t); story.append(Spacer(1,.6*cm))
    story.append(Paragraph("What You Will Learn",S['h2']))
    for item in ["Full Kubernetes workload object hierarchy",
                 "When to choose each workload type (Pod vs Deployment vs StatefulSet…)",
                 "Zero-downtime rolling updates and rollbacks",
                 "Resource requests/limits and Quality-of-Service classes",
                 "HorizontalPodAutoscaler — automatic CPU/memory scaling",
                 "Ready-to-use YAML manifests for every resource type"]:
        story.append(Paragraph(f"✦  {item}",S['bullet']))
    story.append(PageBreak())


def toc(story):
    story.append(Paragraph("Table of Contents",S['h1']))
    story.append(HRFlowable(width="100%",thickness=2,color=BLU,spaceAfter=10))
    rows=[["Ch.","Topic","Key Concepts"],
          ["1","Kubernetes Architecture Overview","Cluster · Node · Pod · Container hierarchy"],
          ["2","Pods — The Atomic Unit","Spec · lifecycle · init/sidecar containers"],
          ["3","ReplicaSets — Desired State","Self-healing · label selectors"],
          ["4","Deployments — The Workhorse","Rolling updates · rollbacks · strategies"],
          ["5","StatefulSets — Stateful Workloads","Ordered pods · stable DNS · per-pod PVCs"],
          ["6","DaemonSets — Node-Level Pods","Logging · monitoring · one pod per node"],
          ["7","Jobs & CronJobs — Batch Workloads","Run-to-completion · scheduled tasks"],
          ["8","HorizontalPodAutoscaler","CPU/memory scaling · stabilization windows"],
          ["9","Resource Management","Requests · limits · QoS classes · LimitRange"],
          ["10","Quick Reference & Cheat Sheet","kubectl commands · comparison tables"]]
    t=Table(rows,colWidths=[1.2*cm,8.3*cm,6*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLU),('TEXTCOLOR',(0,0),(-1,0),WHT),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),9.5),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor("#E8F4FD"),WHT]),
        ('TEXTCOLOR',(0,1),(0,-1),BLU),('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'),
        ('GRID',(0,0),(-1,-1),.5,BOX),('ALIGN',(0,0),(0,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(t); story.append(PageBreak())


def ch1(story):
    story.append(ChapterHeader(1,"Kubernetes Architecture Overview","Cluster → Node → Pod → Container"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("The Kubernetes Object Hierarchy",S['h2']))
    story.append(Paragraph("Every workload ultimately runs as one or more <b>Containers</b> inside a <b>Pod</b>, on a <b>Node</b>, inside a <b>Cluster</b>. Higher-level objects (Deployments, StatefulSets…) manage Pods — you rarely create Pods directly.",S['body']))
    story.append(DiagramF(d_hierarchy()))
    story.append(Paragraph("Figure 1.1 — Kubernetes object nesting: Cluster → Node → Pod → Container(s)",S['caption']))
    rows=[["Object","Managed by","Key property"],
          ["Container","Container runtime (containerd)","Runs the actual process"],
          ["Pod","kubelet on each Node","Shares network + storage between containers"],
          ["ReplicaSet","kube-controller-manager","Maintains N identical Pod copies"],
          ["Deployment","kube-controller-manager","Adds rolling-update + rollback to ReplicaSet"],
          ["StatefulSet","kube-controller-manager","Ordered pods with stable identity + PVCs"],
          ["DaemonSet","kube-controller-manager","One pod per node"],
          ["Job / CronJob","kube-controller-manager","Run-to-completion / scheduled batch"]]
    t=Table(rows,colWidths=[3.5*cm,5.5*cm,6.5*cm]); t.setStyle(_ts()); story.append(t)
    story.append(PageBreak())


def ch2(story):
    story.append(ChapterHeader(2,"Pods — The Atomic Unit","Spec · lifecycle · init containers · sidecar pattern"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("A <b>Pod</b> wraps one or more containers that share the same network namespace (<i>localhost</i>) and optionally the same storage volumes. Pods are <b>ephemeral</b> — they are not rescheduled if a node dies; a controller must do that.",S['body']))
    story.append(Paragraph("Pod Lifecycle",S['h2']))
    story.append(DiagramF(d_pod_lifecycle()))
    story.append(Paragraph("Figure 2.1 — Pod state machine. Liveness probe failure → restart. Readiness probe failure → removed from Service endpoints.",S['caption']))
    story.append(Paragraph("Minimal Pod YAML",S['h2']))
    story.append(CodeBlock("""\
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
    - name: app
      image: nginx:1.27-alpine
      ports:
        - containerPort: 80
      resources:
        requests:
          cpu: 50m
          memory: 64Mi
        limits:
          cpu: 250m
          memory: 128Mi
      readinessProbe:
        httpGet:
          path: /
          port: 80
        initialDelaySeconds: 5
        periodSeconds: 10
      livenessProbe:
        httpGet:
          path: /
          port: 80
        initialDelaySeconds: 15
        periodSeconds: 20""",title="pod.yaml"))
    story.append(Paragraph("InitContainer Pattern",S['h2']))
    story.append(Paragraph("<b>initContainers</b> run sequentially and must all succeed before any regular container starts. Perfect for: waiting for dependencies, running DB migrations, fetching secrets.",S['body']))
    story.append(CodeBlock("""\
spec:
  initContainers:
    - name: wait-for-db
      image: busybox:1.36
      command: [sh,-c,"until nc -z postgres 5432; do sleep 2; done"]
  containers:
    - name: api
      image: my-api:v2""",title="init-container.yaml"))
    story.append(Paragraph("💡 <b>Classroom Question:</b> What happens if an initContainer fails? (Pod restarts per <i>restartPolicy</i>, default: Always. The main containers NEVER start.)",S['callout']))
    story.append(PageBreak())


def ch3(story):
    story.append(ChapterHeader(3,"ReplicaSets — Desired State","Self-healing · label selectors · replica management"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("A <b>ReplicaSet</b> continuously reconciles the <i>desired</i> number of Pod replicas with the <i>actual</i> count. If a Pod is deleted or crashes, the RS creates a replacement. If extras appear with matching labels, the RS deletes them.",S['body']))
    story.append(CodeBlock("""\
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: web-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web        # watches ALL pods with this label
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80""",title="replicaset.yaml"))
    story.append(Paragraph("⚠️ <b>Teaching Note:</b> In practice you never write ReplicaSet YAMLs directly. Always use a <b>Deployment</b> — it manages ReplicaSets for you and adds rolling-update and rollback support.",S['warn']))
    story.append(PageBreak())


def ch4(story):
    story.append(ChapterHeader(4,"Deployments — The Workhorse","Rolling updates · rollbacks · update strategies"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("A <b>Deployment</b> is the most-used workload resource. It wraps a ReplicaSet and adds <b>declarative update semantics</b>: change the image tag in the YAML, apply it, and Kubernetes figures out how to transition safely.",S['body']))
    story.append(Paragraph("Rolling Update — Zero Downtime",S['h2']))
    story.append(DiagramF(d_rolling()))
    story.append(Paragraph("Figure 4.1 — Rolling update v1 → v2. With maxUnavailable:0, traffic is always served by healthy pods.",S['caption']))
    story.append(CodeBlock("""\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # allow 1 extra pod above desired
      maxUnavailable: 0    # no pods go unavailable (zero-downtime)
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine  # change tag to trigger rollout
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 500m
              memory: 128Mi""",title="deployment.yaml"))
    story.append(Paragraph("Key Commands",S['h2']))
    rows=[["Command","Effect"],
          ["kubectl apply -f deployment.yaml","Create or update deployment"],
          ["kubectl set image deploy/web-deploy web=nginx:1.28","Trigger rolling update"],
          ["kubectl rollout status deploy/web-deploy","Watch rollout progress live"],
          ["kubectl rollout undo deploy/web-deploy","Rollback to previous version"],
          ["kubectl rollout history deploy/web-deploy","View change history"],
          ["kubectl scale deploy/web-deploy --replicas=5","Manual scaling"]]
    t=Table(rows,colWidths=[9*cm,6.5*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLU),('TEXTCOLOR',(0,0),(-1,0),WHT),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Courier'),
        ('FONTNAME',(1,1),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor("#E8F4FD"),WHT]),
        ('GRID',(0,0),(-1,-1),.5,BOX),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(t)
    story.append(Paragraph("💡 <b>Lab Exercise:</b> Deploy nginx:1.26, then update to nginx:1.27. Watch the rollout. Then deploy nginx:BROKEN to trigger a failure and practice <i>kubectl rollout undo</i>.",S['callout']))
    story.append(PageBreak())


def ch5(story):
    story.append(ChapterHeader(5,"StatefulSets — Stateful Workloads","Ordered pods · stable hostname · dedicated PVC per pod"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("Use a <b>StatefulSet</b> when your application needs: (1) a stable network identity (<i>pod-0.headless-svc</i>), (2) its own persistent volume per replica, (3) ordered, graceful startup and shutdown.",S['body']))
    story.append(DiagramF(d_statefulset()))
    story.append(Paragraph("Figure 5.1 — StatefulSet: each Pod gets a stable hostname and a dedicated PVC that outlives the Pod.",S['caption']))
    story.append(CodeBlock("""\
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: web-headless   # must match a Headless Service
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          volumeMounts:
            - name: data
              mountPath: /data
  volumeClaimTemplates:        # 1 PVC per Pod, created automatically
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 1Gi""",title="statefulset.yaml"))
    rows=[["Feature","Deployment","StatefulSet"],
          ["Pod names","Random (deploy-abc)","Stable (web-0, web-1, web-2)"],
          ["Startup order","Parallel","Sequential: 0 then 1 then 2"],
          ["DNS hostname","Not stable","web-0.web-headless.ns.svc"],
          ["Per-pod storage","Shared or none","Dedicated PVC per Pod"],
          ["Use cases","APIs, frontends","Postgres, Redis, Kafka, Zookeeper"]]
    t=Table(rows,colWidths=[4*cm,5.5*cm,6*cm])
    t.setStyle(_ts([('TEXTCOLOR',(0,1),(0,-1),BLU),('FONTNAME',(0,1),(0,-1),'Helvetica-Bold')])); story.append(t)
    story.append(PageBreak())


def ch6(story):
    story.append(ChapterHeader(6,"DaemonSets — Node-Level Pods","One Pod per Node · auto-scheduled on new nodes"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("A <b>DaemonSet</b> guarantees that one copy of a Pod runs on <b>every Node</b> (or a subset via nodeSelector/tolerations). When a new node joins the cluster the Pod is automatically scheduled onto it.",S['body']))
    story.append(DiagramF(d_daemonset()))
    story.append(Paragraph("Figure 6.1 — DaemonSet places one Pod per Node; new nodes receive the Pod automatically.",S['caption']))
    rows=[["Use Case","Example Tools"],
          ["Node-level log collection","Fluentd, Fluent Bit, Filebeat"],
          ["Node monitoring agent","Prometheus node-exporter, Datadog Agent"],
          ["CNI network plugin","Calico, Cilium, Flannel"],
          ["Distributed storage daemon","Rook/Ceph, GlusterFS"],
          ["Security / runtime scanning","Falco, Sysdig, Tetragon"]]
    t=Table(rows,colWidths=[7*cm,8.5*cm]); t.setStyle(_ts()); story.append(t)
    story.append(Spacer(1,.3*cm))
    story.append(CodeBlock("""\
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-logger
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: node-logger
  template:
    metadata:
      labels:
        app: node-logger
    spec:
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          effect: NoSchedule
      containers:
        - name: fluent-bit
          image: fluent/fluent-bit:3.0
          resources:
            limits:
              memory: 128Mi
              cpu: 100m
          volumeMounts:
            - name: varlog
              mountPath: /var/log
      volumes:
        - name: varlog
          hostPath:
            path: /var/log""",title="daemonset.yaml"))
    story.append(PageBreak())


def ch7(story):
    story.append(ChapterHeader(7,"Jobs & CronJobs — Batch Workloads","Run-to-completion · automatic retries · scheduled tasks"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("<b>Jobs</b> create one or more Pods and track them until completion. Completed Pods are <i>not</i> restarted. Failed Pods are retried up to <i>backoffLimit</i> times.",S['body']))
    story.append(DiagramF(d_job()))
    story.append(Paragraph("Figure 7.1 — Job lifecycle: Pod failure triggers retry; success marks Job Complete.",S['caption']))
    story.append(CodeBlock("""\
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
spec:
  completions: 1       # total successful completions required
  parallelism: 1       # pods running in parallel
  backoffLimit: 3      # max retries on failure
  template:
    spec:
      restartPolicy: OnFailure  # Never or OnFailure (not Always)
      containers:
        - name: migrate
          image: my-app:v2
          command: [python, manage.py, migrate]""",title="job.yaml"))
    story.append(Paragraph("CronJobs — Scheduled Jobs",S['h2']))
    story.append(Paragraph("A <b>CronJob</b> creates a new Job on a cron schedule. It uses standard Unix cron syntax.",S['body']))
    story.append(CodeBlock("""\
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-report
spec:
  schedule: "0 2 * * *"      # every day at 02:00 UTC
  concurrencyPolicy: Forbid  # skip new Job if previous still running
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: report
              image: my-reporter:v1
              command: [python, report.py]""",title="cronjob.yaml"))
    story.append(Paragraph("💡 <b>Lab Idea:</b> Create a CronJob that runs every minute (<i>* * * * *</i>), watch pods appear with <i>kubectl get pods -w</i>, then inspect completed pods with <i>kubectl logs</i>.",S['callout']))
    story.append(PageBreak())


def ch8(story):
    story.append(ChapterHeader(8,"HorizontalPodAutoscaler","CPU & memory scaling · min/max replicas · stabilization"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("The <b>HPA</b> automatically adjusts the number of Pod replicas based on observed metrics (CPU, memory, or custom). It reads data from the <b>Metrics Server</b> every 15 seconds and calculates:",S['body']))
    story.append(Paragraph("desiredReplicas = ceil(currentReplicas × currentMetric / targetMetric)",ParagraphStyle('F',fontName='Courier-Bold',fontSize=10,textColor=BLU,backColor=colors.HexColor("#E8F4FD"),borderPad=6,spaceAfter=8,spaceBefore=4,leftIndent=20)))
    story.append(DiagramF(d_hpa()))
    story.append(Paragraph("Figure 8.1 — HPA reads CPU from Metrics Server and scales the Deployment.",S['caption']))
    story.append(CodeBlock("""\
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deploy
  minReplicas: 2
  maxReplicas: 8
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60   # scale up when avg CPU > 60%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 75
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60    # wait 1 min before scaling up
    scaleDown:
      stabilizationWindowSeconds: 300   # wait 5 min before scaling down""",title="hpa.yaml"))
    story.append(Paragraph("⚠️ <b>Prerequisite:</b> HPA requires the <b>Metrics Server</b> to be installed. On minikube: <i>minikube addons enable metrics-server</i>. Without it, HPA shows <Unknown> for current CPU.",S['warn']))
    story.append(PageBreak())


def ch9(story):
    story.append(ChapterHeader(9,"Resource Management","Requests · Limits · QoS Classes · LimitRange"))
    story.append(Spacer(1,.3*cm))
    story.append(DiagramF(d_resources()))
    story.append(Paragraph("Figure 9.1 — Requests are used for scheduling; limits are enforced at runtime.",S['caption']))
    story.append(Paragraph("Requests vs Limits",S['h2']))
    rows=[["",  "Request","Limit"],
          ["CPU","Guaranteed minimum. Used by scheduler to find a node with enough free CPU.","Hard ceiling. Container is CPU-throttled if it tries to exceed this."],
          ["Memory","Guaranteed minimum. Scheduler uses this for placement.","Hard ceiling. Container is OOMKilled if it exceeds this."]]
    t=Table(rows,colWidths=[2*cm,7*cm,6.5*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLU),('TEXTCOLOR',(0,0),(-1,0),WHT),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),.5,BOX),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor("#E8F4FD"),WHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(t)
    story.append(Paragraph("QoS Classes",S['h2']))
    rows=[["QoS Class","Condition","Eviction Priority (low = evicted first)"],
          ["BestEffort","No requests or limits set","Evicted first under pressure"],
          ["Burstable","Requests set, limits > requests (or no limits)","Middle priority"],
          ["Guaranteed","Requests == Limits for ALL containers","Last to be evicted"]]
    t=Table(rows,colWidths=[3*cm,6.5*cm,6*cm]); t.setStyle(_ts())
    story.append(t)
    story.append(Paragraph("LimitRange — Cluster Defaults",S['h2']))
    story.append(Paragraph("A <b>LimitRange</b> sets default requests/limits for a namespace so Pods without explicit resources still get sensible values.",S['body']))
    story.append(CodeBlock("""\
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: default
spec:
  limits:
    - type: Container
      default:          # applied as limit if none specified
        cpu: 500m
        memory: 128Mi
      defaultRequest:   # applied as request if none specified
        cpu: 100m
        memory: 64Mi
      max:              # pods cannot exceed these
        cpu: 2
        memory: 1Gi""",title="limitrange.yaml"))
    story.append(PageBreak())


def ch10(story):
    story.append(ChapterHeader(10,"Quick Reference & Cheat Sheet","kubectl commands · workload comparison"))
    story.append(Spacer(1,.3*cm))
    story.append(Paragraph("Workload Comparison at a Glance",S['h2']))
    rows=[["Workload","Replicas?","Ordered?","Stable ID?","Persistent Storage?","Use when…"],
          ["Pod","No","—","No","Shared only","Quick testing only"],
          ["ReplicaSet","Yes","No","No","Shared only","(use Deployment instead)"],
          ["Deployment","Yes","No","No","Shared only","Stateless services, APIs, frontends"],
          ["StatefulSet","Yes","Yes","Yes","Per-pod PVC","Databases, message queues"],
          ["DaemonSet","1/node","No","No","HostPath/shared","Logging, monitoring agents"],
          ["Job","Configurable","No","No","Shared only","Batch tasks, DB migrations"],
          ["CronJob","Configurable","No","No","Shared only","Scheduled batch tasks"]]
    t=Table(rows,colWidths=[2.5*cm,2*cm,2*cm,2.2*cm,2.8*cm,4*cm])
    t.setStyle(_ts([('FONTSIZE',(0,0),(-1,-1),8),('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'),
                    ('TEXTCOLOR',(0,1),(0,-1),BLU)]))
    story.append(t)
    story.append(Spacer(1,.4*cm))
    story.append(Paragraph("Essential kubectl Commands",S['h2']))
    rows=[["Command","Description"],
          ["kubectl get pods -n <ns> -w","Watch pods live"],
          ["kubectl describe pod <name>","Show events, probes, resource limits"],
          ["kubectl logs -f deploy/<name>","Stream logs from deployment"],
          ["kubectl exec -it <pod> -- sh","Shell into a pod"],
          ["kubectl apply -f file.yaml","Create or update any resource"],
          ["kubectl delete -f file.yaml","Delete resources from file"],
          ["kubectl rollout status deploy/<name>","Monitor a rolling update"],
          ["kubectl rollout undo deploy/<name>","Rollback one revision"],
          ["kubectl scale deploy/<name> --replicas=4","Manual scale"],
          ["kubectl top pods","Show CPU/memory usage (needs Metrics Server)"],
          ["kubectl get events --sort-by=.lastTimestamp","Debug cluster events"]]
    t=Table(rows,colWidths=[9.5*cm,6*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLU),('TEXTCOLOR',(0,0),(-1,0),WHT),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Courier'),
        ('FONTNAME',(1,1),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor("#E8F4FD"),WHT]),
        ('GRID',(0,0),(-1,-1),.5,BOX),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(t)
    story.append(Spacer(1,.4*cm))
    story.append(Paragraph("💡 <b>Final Classroom Challenge:</b> Students deploy the full Job Board lab (from the DevSecOps project) to a minikube cluster using only manifests from the k8s/ directory — no docker-compose allowed!",S['callout']))
