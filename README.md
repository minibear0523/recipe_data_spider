# Diet Database
## Recipe Table
CREATE TABLE fittime_recipe (
    id serial PRIMARY KEY,
    article_id integer,
    user_id integer,
    title text,
    description text,
    category text,
    comment_count integer,
    praise_count integer,
    view_count integer,
    collection_count integer,
    create_time date,
    update_time date,
    content text,
    content_url text,
    contains_video boolean,
    rank integer,
    image_url text,
    kind varchar(10),
    db_create_time timestamp
);

## Activity Table
CREATE TABLE fittime_activity (
    id serial PRIMARY KEY,
    activity_id integer,
    user_id integer,
    checkin_id integer,
    link_id integer,
    content text,
    create_time date,
    update_time date,
    video_url text,
    total_comment integer,
    total_praise integer,
    is_topic_selected boolean,
    db_create_time timestamp
);