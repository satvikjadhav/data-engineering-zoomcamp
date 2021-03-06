## Terraform and GCP Notes

### Introduction
	-What is Terraform?
	-open-source tool by HashiCorp, used for provisioning infrastructure resources
	-supports DevOps best practices for change management
	-Managing configuration files in source control to maintain an ideal provisioning state for testing and production environments
	-Provides a consistent CLI workflow to manage hundreds of cloud services.
	-Manage infra with config files

The idea of Terraform is to have repeatable infrastructure. 
If you build solely through the web interface, you will have a tough time reproducing the infrastructure with the same configuration as the architecture evolves over time. 
As a result, your infrastructure is now version controlled.

Best example I can give you for why the reproducibility is useful is the necessity to replicate a particular system's infrastructure in both dev and prod environments. 
You do it once for dev, then you just need to do a few commands to replicate the entire thing in prod.

Second example, perhaps your company has initiative to experiment on the existing infrastructure that has been 'terraformed'. 
Well now, you can reproduce the existing infra and experiment on this instead.

### What is IaC?
	-Infrastructure-as-Code
	-build, change, and manage your infrastructure in a safe, consistent, and repeatable way by defining resource configurations that you can version, reuse, and share.
	-Like a git version control system but for infrastructure
### Some advantages
	-Infrastructure lifecycle management
	-Build, change, and destroy infrastructure with Terraform.
	-Version control commits
	-Very useful for stack-based deployments, and with cloud providers such as AWS, GCP, Azure, K8S…
	-State-based approach to track resource changes throughout deployments

Most important part about terraform is the terraform state.
Which allows us to track resource changes throughout the deployment

### To use gcloud do the following steps:
  1. Download gcloud SDK
  2. install it via the install.sh or install.bat files
  3. If in windows add a path to your python folder
  4. Create a variable to store your service account key that you generated
    - export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json
  5. Now authenticate:
    - gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
  6. or we can use this as well:
	gcloud auth application-default login

### Now we create two infra modules in GCP (Google Cloud Platform)with Terraform
	- Google Cloud Storage: Data Lake
	- BigQueyr: Data Warehouse

In production we would create custom roles in GCP

Creating GCP Infra with Terraform

### Declarations
  - terraform: configure basic Terraform settings to provision your infrastructure
	- required_version: minimum Terraform version to apply to your configuration
	- backend: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
		- local: stores state file locally as terraform.tfstate
	- required_providers: specifies the providers required by the current module
- provider:
	- adds a set of resource types and/or data sources that Terraform can manage
	- The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
- resource
	- blocks to define components of your infrastructure
	- Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
- variable & locals
	- runtime arguments and constants

We make use of two files: main.tf and variables.tf

- terraform deleration defines your terraform version
- backend shows where the terraform is stored (gcp, aws services)
- required_providers - this is optional 
	- In python context, we can think of this as importing a library

- Terraform relies on plugins called "providers" to interact with cloud providers, saas providers and other APIs

- Resource: physical component such as a server, storage, stoarge bucket, or a data warehouse. 

"locals" keyword in the variables.tf file are equivalent of constants
	- Any time within your setup you're referring to a particular variable, you will be able to access it if it is in your local folders

- Variables: are something that are generally passted at runtime. 
	- Variables without default keywords are mandatory at runtime, and variables with default keywords are optional

The following variables are being used:
1. variable "project"
2. variable "region"
3. variable "storage_class"
4. variable "BQ_DATASET"

It is a good practice to keep all the resources that we use in one region.
	- If our resources are spread accross different regions there could be issues with communications between our resources

**terraform init**:
- Initializes and installs the required plugins for example google providers, and existing configs from the web for the respective cloud provider

**terraform plan**:
- A command to show the execution plan. 
- Describes the actions the terraform will take in order to create the infracture to match with the configuration

**terraform apply**:
- Detects whatever changes that may have been made by using the terraform plan command
	- Any resources to be deleted
	- Any new resources to be created
	- Any existing resources or modules that need to be updated

Sample terraform apply command:

### Terraform will perform the following actions:
```
  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "asia-south1"
      + project                    = "ny-rides-satvik"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "ASIA-SOUTH1"
      + name                        = "dtc_data_lake_ny-rides-satvik"
      + project                     = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_storage_class = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

     Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  google_bigquery_dataset.dataset: Creating...
  google_storage_bucket.data-lake-bucket: Creating...
  google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dtc_data_lake_data-engineering-339113]
  google_bigquery_dataset.dataset: Creation complete after 4s [id=projects/data-engineering-339113/datasets/trips_data_all]
```
#### The beauty of this is that we were able to create 3 different resources/services within one second. How crazy is that?!?


### terraform destroy:
	- In any development enviornment, we do not want to keep our resources set up on our cloud and leave them idle and running
	- Used to destory or close these resources

sample terraform destroy command being used:

 - destroy

### Terraform will perform the following actions:
```
  # google_bigquery_dataset.dataset will be destroyed
  - resource "google_bigquery_dataset" "dataset" {
      - creation_time                   = 1643047399213 -> null
      - dataset_id                      = "trips_data_all" -> null
      - default_partition_expiration_ms = 0 -> null
      - default_table_expiration_ms     = 0 -> null
      - delete_contents_on_destroy      = false -> null
      - etag                            = "LSxyTOuyRQR70GCaDdBuMw==" -> null
      - id                              = "projects/data-engineering-339113/datasets/trips_data_all" -> null
      - labels                          = {} -> null
      - last_modified_time              = 1643047399213 -> null
      - location                        = "asia-south1" -> null
      - project                         = "data-engineering-339113" -> null
      - self_link                       = "https://bigquery.googleapis.com/bigquery/v2/projects/data-engineering-339113/datasets/trips_data_all" -> null

      - access {
          - role          = "OWNER" -> null
          - user_by_email = "data-engineering-user@data-engineering-339113.iam.gserviceaccount.com" -> null
        }
      - access {
          - role          = "OWNER" -> null
          - special_group = "projectOwners" -> null
        }
      - access {
          - role          = "READER" -> null
          - special_group = "projectReaders" -> null
        }
      - access {
          - role          = "WRITER" -> null
          - special_group = "projectWriters" -> null
        }
    }

  # google_storage_bucket.data-lake-bucket will be destroyed
  - resource "google_storage_bucket" "data-lake-bucket" {
      - default_event_based_hold    = false -> null
      - force_destroy               = true -> null
      - id                          = "dtc_data_lake_data-engineering-339113" -> null
      - labels                      = {} -> null
      - location                    = "ASIA-SOUTH1" -> null
      - name                        = "dtc_data_lake_data-engineering-339113" -> null
      - project                     = "data-engineering-339113" -> null
      - requester_pays              = false -> null
      - self_link                   = "https://www.googleapis.com/storage/v1/b/dtc_data_lake_data-engineering-339113" -> null
      - storage_class               = "STANDARD" -> null
      - uniform_bucket_level_access = true -> null
      - url                         = "gs://dtc_data_lake_data-engineering-339113" -> null

      - lifecycle_rule {
          - action {
              - type = "Delete" -> null
            }

          - condition {
              - age                        = 30 -> null
              - days_since_custom_time     = 0 -> null
              - days_since_noncurrent_time = 0 -> null
              - matches_storage_class      = [] -> null
              - num_newer_versions         = 0 -> null
              - with_state                 = "ANY" -> null
            }
        }

      - versioning {
          - enabled = true -> null
        }
    }

	Plan: 0 to add, 0 to change, 2 to destroy.

	Do you really want to destroy all resources?
	  Terraform will destroy all your managed infrastructure, as shown above.
	  There is no undo. Only 'yes' will be accepted to confirm.

	  Enter a value: yes

	google_storage_bucket.data-lake-bucket: Destroying... [id=dtc_data_lake_data-engineering-339113]
	google_bigquery_dataset.dataset: Destroying... [id=projects/data-engineering-339113/datasets/trips_data_all]
	google_storage_bucket.data-lake-bucket: Destruction complete after 1s
	google_bigquery_dataset.dataset: Destruction complete after 1s
```

#### .terraform folder is essentially a package manager
