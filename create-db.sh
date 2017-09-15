# run this as postgres user, eg:
# imposm-psqldb > create_db.sh; sudo su postgres; sh ./create_db.sh

# Print commands and their arguments as they are executed (-x) and Exit immediately if a command exits with a non-zero exit status.
set -xe
# Create a user called 'osm' who can create db but he's not a superuser and cannot create role
createuser --no-superuser --no-createrole --createdb osm
# Create a db, named 'osmlanduse', encoded in UTF-8, owned by 'osm'
createdb -E UTF8 -O osm osmlanduse
# Run some postgresql commands (-c) to the db 'osmlanduse' (-d)
psql -d osmlanduse -c "alter user osm with password 'osm';"
psql -d osmlanduse -c "create extension postgis;"
psql -d osmlanduse -f /media/julien/data/Projets/Geomatique/OSM/Mapnik/venv/local/lib/python2.7/site-packages/imposm/900913.sql
echo "ALTER TABLE geometry_columns OWNER TO osm;" | psql -d osmlanduse
echo "ALTER TABLE spatial_ref_sys OWNER TO osm;" | psql -d osmlanduse
echo "ALTER USER osm WITH PASSWORD 'osm';" |psql -d osmlanduse
echo "host osm	osmlanduse	127.0.0.1/32	md5" >> /etc/postgresql/9.5/main/pg_hba.conf 	# <- CHANGE THIS PATH
set +x
echo "Done. Don't forget to restart postgresql!"
