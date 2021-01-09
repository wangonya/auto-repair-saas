# auto-repair-saas

![Django CI](https://github.com/wangonya/auto-repair-saas/workflows/Django%20CI/badge.svg)
<a href="https://codeclimate.com/github/wangonya/auto-repair-saas/maintainability"><img src="https://api.codeclimate.com/v1/badges/a49ef56b072d01dc4c30/maintainability" /></a>
<a href="https://codeclimate.com/github/wangonya/auto-repair-saas/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a49ef56b072d01dc4c30/test_coverage" /></a>

A cloud-based auto repair shop management
software. <a href="https://auto-repair-saas-3exc8.ondigitalocean.app" target="_blank">Deployed on Digital Ocean.</a>

Some aspects of the system are specific to my locality. They can of course be removed or adapted to fit different
requirements.

## Modules

### Dashboard

- Displays three metrics at the moment:
    1. **Sales**. When a payment is registered for a job, that info is recorded as a sale for that day and reflects on
       the sales chart. In addition to the amount, the payment method is also recorded and displayed on the chart. The
       payment method can be *Cash*, *Card* or *M-Pesa (a local mobile money transfer service)*.
    2. **Top Earners**. Connected to sales. Each job should have a staff member assigned to it. As we keep track of
       sales, we also keep track of the staff members attached to the related sales, and display the top 5 in this
       section.
    3. **Jobs Overview**. Tracks the jobs created over the selected period. *Note: Generating demo data for testing
       makes it seem like you have data created over a period of time, but because all that data was created at the
       moment you generated it, this section will show the same data for 'Week', 'Month' and 'Year' (assuming the
       generated data is the only data you have so far)*.

### Jobs

- CRUD operations for jobs. Jobs be of different categories:
    1. **Estimates**.
        * Before a car is worked on, the client is given an estimate of the cost. At this stage the estimate is '
          pending'. Payment can not be registered while an estimate is pending.
        * If the client confirms that they want to move forward, the estimate becomes 'confirmed'.
    2. **In Progress**. These are jobs that are currently being worked on.
    3. **Done**. Jobs that have been completed.

### Contacts

- CRUD operations for contacts. Contacts can either be 'clients' or 'suppliers'. Suppliers don't serve any purpose at
  the moment.

### Vehicles

- CRUD operations for vehicles.

### Staff

- CRUD operations for staff.

## [Todos](https://github.com/wangonya/auto-repair-saas/projects/1#column-12169588)