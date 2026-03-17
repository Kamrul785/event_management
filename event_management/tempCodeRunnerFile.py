DATABASES = {
    'default': dj_database_url.config(
        default=database_url or f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=is_supabase_database,
    )
}