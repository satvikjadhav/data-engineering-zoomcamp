# Dataproc Cluster Setup

***Dataproc*** is a service offered on the Google Cloud Platform
```It is a fully managed and highly scalable service for running Apache Spark, Apache Flink, Presto, and 30+ open source tools and frameworks. Use Dataproc for data lake modernization, ETL, and secure data science, at planet scale, fully integrated with Google Cloud, at a fraction of the cost.```

**Pricing**

Dataproc pricing is based on the number of vCPU and the duration of time that they run. While pricing shows hourly rate, we charge down to the second, so you only pay for what you use.

Ex: 6 clusters (1 main + 5 workers) of 4 CPUs each ran for 2 hours would cost $.48.  Dataproc charge = # of vCPUs * hours * Dataproc price = 24 * 2 * $0.01 = $0.48

## Creating a Cluster

1. Go to Dataproc service page in GCP
2. Click on `Create Cluster`
3. Location should same as the location of our Google Cloud Storage Bucket
4. In additional components, we can select whichever software we want our dataproc cluster to come installed with
5. For now we can go with all default
6. Click on `create`

To use code with dataproc, we will have to
- add a folder called `code` in our bucket
- add our python script with pyspark code in `code` bucket using the following command
```bash
gsutil cp code.py gs://bucket_name/code/code.py
```

If we want to do this trough CLI or through Airflow, we would need to use Google SDK

We can also submit a job through REST API, and to do this we would need to get the information from the `Equivalent REST` button under the `Job Details` tab

Useful [documentation](https://cloud.google.com/dataproc/docs/guides/submit-job) for submitting a job to a Dataproc cluster

Example:
```bash
gcloud dataproc jobs submit pyspark \
    --cluster=cluster-name \
    --region=region \
    location_of_the_script_in_cloud \
    -- job-args
```

After using this we might get `PERMISSION DENIED`, and the reason for this is because we might be using a service account that ***does not have permissions to submit jobs to dataproc***

We can solve this problem by giving the account the appropriate permission, in our case `Dataproc Administrator`, in the `IAM` tab