-- Migration: 001_add_note_table.sql
-- Simple schema for storing user notes. Created for learning purposes, not intended for production use.

CREATE TABLE IF NOT EXISTS Note (
	id SERIAL PRIMARY KEY,
	user_id VARCHAR(255) NOT NULL,
	content TEXT NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
);