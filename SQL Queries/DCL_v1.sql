-- 1. API role: read/write data already in app_schema
CREATE ROLE app_api LOGIN PASSWORD 'api_123';
GRANT USAGE ON SCHEMA app_schema TO app_api;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app_schema TO app_api;
ALTER DEFAULT PRIVILEGES IN SCHEMA app_schema
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_api;

-- 2. Schema editor: can change tables/indexes/etc. inside app_schema
CREATE ROLE app_schema_editor LOGIN PASSWORD 'schemaeditor888';
GRANT USAGE, CREATE ON SCHEMA app_schema TO app_schema_editor;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA app_schema TO app_schema_editor;
ALTER DEFAULT PRIVILEGES IN SCHEMA app_schema
    GRANT ALL ON TABLES TO app_schema_editor;

-- 3. Read-only role: can only query data
CREATE ROLE app_readonly LOGIN PASSWORD 'readonly123';
GRANT USAGE ON SCHEMA app_schema TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA app_schema TO app_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA app_schema
    GRANT SELECT ON TABLES TO app_readonly;

REVOKE ALL ON SCHEMA app_schema FROM PUBLIC;
REVOKE CREATE ON DATABASE postgres FROM PUBLIC;
