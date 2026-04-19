-- Migration: 002_note_with_server_id.sql
-- Adds a server_id column to the Note table

ALTER TABLE Note ADD COLUMN server_id VARCHAR(255) DEFAULT NULL;
