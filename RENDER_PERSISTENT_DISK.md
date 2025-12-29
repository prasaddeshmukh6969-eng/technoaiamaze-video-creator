# Render Persistent Disk Configuration
# This file tells Render to create a persistent disk so users.json survives restarts

# Add this to your render.yaml
services:
  - type: web
    name: technoaiamaze-video-creator
    runtime: python
    buildCommand: "pip install -r server/requirements-mock.txt"
    startCommand: "cd server && python mock_server.py"
    disk:
      name: technoaiamaze-data
      mountPath: /opt/render/project/src/server/data
      sizeGB: 1

# This configuration:
# 1. Creates a 1GB persistent disk
# 2. Mounts it at /server/data directory
# 3. Data persists across restarts and deploys
# 4. Free tier includes persistent disks!

# Alternative: Store users.json in GitHub (encrypted)
# See server/scripts/backup_users.py for automated backup
