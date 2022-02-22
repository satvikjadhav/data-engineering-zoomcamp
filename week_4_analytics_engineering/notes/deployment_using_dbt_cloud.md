## Deployment of a dbt Project

Now that we have completed a complete project, and tested and documented it, and know that everything runs properly. Its time to deploy it. 

### What is Deployment?

- Process of running the models we created in our development environment in a production environment
- Development and later deployment allows us to continue building models and testing them without affecting our production environment
- A deployment environment will normally have different schema in our data warehouse and ideally a different user
-Development workflow:
- Develop in a user branch
- Open a PR to merge into the main branch
- Run the new models in the production environment using the main branch (Version control and CI/CD)
- Schedule the models

### Running a dbt project in production

- dbt cloud includes a scheduler where to create jobs to run in production
- A single job can run multiple commands
- Jobs can be triggered manually or on schedule
- Each job will keep a log of the runs over time
- Each run will have the logs for each command
- A job could also generate documentation, that could be viewed under the run information
- If dbt source freshness was run, the results can also be viewed at the end of a job

### What is Continuous Integration (CI)?

- CI is the practice of regularly merging development brances into a central repository, after which automated builds and tests are run
- The goal is to reduce adding bugs to the production code and maintain a more stable project
- dbt allows us to enable CI on pull requests
- Enabled via webhooks from GitHub or GitLab
- When a PR is read to be merged, a webhook is recieved in dbt Cloud that will enqueue a new run of the specified job
- The run of the CI job will be against a temporary schema
- No PR will be able to be merged unless the run has been completed successfully

We can then add the following after `dev` in our profiles.yml
```yaml
prod:
  dataset: production_dataset (this is schema)
  fixed_retries: 1
  keyfile: /.google/credentials/google_credentials.json
  location: EU
  method: service-account
  priority: interactive
  project: data-engineering-339113
  threads: 2
  timeout_seconds: 300
  type: bigquery
```
Since we have `target: dev`, anytime we run `dbt build` it will run agianst our dev settings. 
To run in production db, we should run: `dbt build -t prod`
- `-t`: target

And we can use `cron` as well as `airflow` to schedule these jobs 

