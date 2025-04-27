
#!/bin/bash

echo "stopping all services"

kill $(ps aux | grep "python")

echo "stopping all services done"