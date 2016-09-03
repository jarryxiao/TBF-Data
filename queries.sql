/** SQL queries that might be of interest. Copy and paste into

/* Attendance rate for each event. */
select event_name, round(r, 4)
from (
    select event_name, (cast(count(case when attendee_status like 'Checked In' then 1 end) as FLOAT) / cast(count(*) as FLOAT)) as r
    from attendees
    group by event_name
)
order by r desc;

/** Average attendance rate overall and variance (because sqlite doesn't have sqrt). */
select avg(r), ((sum(r)*sum(r) - sum(r * r))/((count(*)-1)*(count(*))))
from (
    select event_name, (cast(count(case when attendee_status like 'Checked In' then 1 end) as FLOAT) / cast(count(*) as FLOAT)) as r
    from attendees
    group by event_name
)
order by r desc;

/** Events by number checked in. */
select event_name, count(*)
from attendees
where attendee_status like "Checked In"
group by event_name
order by count(*) desc;

/** Average checked in for all events. */
select avg(c)
from (
    select event_name, count(*) as c
    from attendees
    where attendee_status like "Checked In"
    group by event_name
    order by count(*) desc
);

/** How did people hear about events? */
select how_did_you_hear, count(*)
from attendees
group by how_did_you_hear
order by count(*) desc;

/** Attendance rate for how people heard about events. */
select how_did_you_hear, c, round(r, 4)
from (
    select how_did_you_hear, count(*) as c, (cast(count(case when attendee_status like 'Checked In' then 1 end) as FLOAT) / cast(count(*) as FLOAT)) as r
    from attendees
    group by how_did_you_hear
    having count(*) > 5
)
order by r desc;

/** Events by signups. */
select event_name, count(*) as c
from attendees
group by event_name
order by count(*) desc;

/** Average event signups. */
select avg(c)
from (
    select count(*) as c
    from attendees
    group by event_name
);

/** Attendees who have paid the most to attend events. */
select first_name, last_name, email, sum(total_paid)
from attendees
where total_paid > 0
group by first_name, last_name
order by sum(total_paid) desc;

/** People who have attended the most events. */
select first_name, last_name, email, count(*)
from attendees
group by first_name, last_name
order by count(*) desc;

/** Number of people who paid money for events and had a Berkeley email and how much they paid. */
select count(*), sum(total_paid)
from attendees
where email like '%@berkeley%' and total_paid > 0;

/** Total ticket sales ($). */
select sum(total_paid)
from attendees;

/** Ticket sales by event ($). */
select event_name, sum(total_paid)
from attendees
group by event_name
order by sum(total_paid) desc;

/** Number of tickets sold for each ticket type. */
select ticket_type, count(*)
from attendees
group by ticket_type
order by count(*) desc;

/** Ticket sales by IP location. */
select ip_location, count(*)
from attendees
group by ip_location
order by count(*) desc;

/** Number of people who bought tickets from IPs outside of California. */
select count(*)
from attendees
where ip_location not like '% CA, %';

/* People who bought tickets from outside CA who checked in. */
select count(*)
from attendees
where ip_location not like '% CA, %' and attendee_status like "Checked In";

/* Events by attendees from outside CA. */
select event_name, count(*)
from attendees
where ip_location not like '% CA, %' and attendee_status like "Checked In"
group by event_name
order by count(*) desc;
