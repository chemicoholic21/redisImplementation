"""
Simple Redis operations examples.
Demonstrates basic Redis functionality with Python.
"""
import redis
import json
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_USERNAME


class RedisClient:
    """Simple Redis client wrapper."""
    
    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                username=REDIS_USERNAME,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            print(f"✅ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        except redis.ConnectionError:
            print(f"❌ Failed to connect to Redis at {REDIS_HOST}:{REDIS_PORT}")
            print("Make sure Redis server is running or check your credentials!")
            self.redis_client = None
    
    def is_connected(self):
        """Check if Redis connection is active."""
        return self.redis_client is not None
    
    def set_string(self, key, value, expire_seconds=None):
        """Store a string value in Redis."""
        if not self.is_connected():
            return False
        
        try:
            self.redis_client.set(key, value, ex=expire_seconds)
            print(f"✅ Stored: {key} = {value}")
            if expire_seconds:
                print(f"   (expires in {expire_seconds} seconds)")
            return True
        except Exception as e:
            print(f"❌ Error storing {key}: {e}")
            return False
    
    def get_string(self, key):
        """Retrieve a string value from Redis."""
        if not self.is_connected():
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                print(f"✅ Retrieved: {key} = {value}")
            else:
                print(f"❌ Key not found: {key}")
            return value
        except Exception as e:
            print(f"❌ Error retrieving {key}: {e}")
            return None
    
    def set_json(self, key, data, expire_seconds=None):
        """Store JSON data in Redis."""
        if not self.is_connected():
            return False
        
        try:
            json_str = json.dumps(data)
            self.redis_client.set(key, json_str, ex=expire_seconds)
            print(f"✅ Stored JSON: {key} = {data}")
            return True
        except Exception as e:
            print(f"❌ Error storing JSON {key}: {e}")
            return False
    
    def get_json(self, key):
        """Retrieve JSON data from Redis."""
        if not self.is_connected():
            return None
        
        try:
            json_str = self.redis_client.get(key)
            if json_str:
                data = json.loads(json_str)
                print(f"✅ Retrieved JSON: {key} = {data}")
                return data
            else:
                print(f"❌ Key not found: {key}")
                return None
        except Exception as e:
            print(f"❌ Error retrieving JSON {key}: {e}")
            return None
    
    def add_to_list(self, key, value):
        """Add value to a Redis list."""
        if not self.is_connected():
            return False
        
        try:
            self.redis_client.lpush(key, value)
            print(f"✅ Added to list {key}: {value}")
            return True
        except Exception as e:
            print(f"❌ Error adding to list {key}: {e}")
            return False
    
    def get_list(self, key, start=0, end=-1):
        """Get all values from a Redis list."""
        if not self.is_connected():
            return []
        
        try:
            values = self.redis_client.lrange(key, start, end)
            print(f"✅ List {key}: {values}")
            return values
        except Exception as e:
            print(f"❌ Error getting list {key}: {e}")
            return []
    
    def set_hash(self, key, field, value):
        """Set a field in a Redis hash."""
        if not self.is_connected():
            return False
        
        try:
            self.redis_client.hset(key, field, value)
            print(f"✅ Set hash {key}[{field}] = {value}")
            return True
        except Exception as e:
            print(f"❌ Error setting hash {key}: {e}")
            return False
    
    def get_hash(self, key, field=None):
        """Get field(s) from a Redis hash."""
        if not self.is_connected():
            return None
        
        try:
            if field:
                value = self.redis_client.hget(key, field)
                print(f"✅ Hash {key}[{field}] = {value}")
                return value
            else:
                values = self.redis_client.hgetall(key)
                print(f"✅ Hash {key}: {values}")
                return values
        except Exception as e:
            print(f"❌ Error getting hash {key}: {e}")
            return None
    
    def delete_key(self, key):
        """Delete a key from Redis."""
        if not self.is_connected():
            return False
        
        try:
            result = self.redis_client.delete(key)
            if result:
                print(f"✅ Deleted key: {key}")
            else:
                print(f"❌ Key not found: {key}")
            return result
        except Exception as e:
            print(f"❌ Error deleting {key}: {e}")
            return False
    
    def get_all_keys(self, pattern="*"):
        """Get all keys matching a pattern."""
        if not self.is_connected():
            return []
        
        try:
            keys = self.redis_client.keys(pattern)
            print(f"✅ Found {len(keys)} keys matching '{pattern}': {keys}")
            return keys
        except Exception as e:
            print(f"❌ Error getting keys: {e}")
            return []


def demo_basic_operations():
    """Demonstrate basic Redis operations."""
    print("\n🔗 Redis Basic Operations Demo")
    print("=" * 40)
    
    # Initialize Redis client
    redis_client = RedisClient()
    
    if not redis_client.is_connected():
        return
    
    # String operations
    print("\n📝 String Operations:")
    redis_client.set_string("greeting", "Hello Redis!")
    redis_client.get_string("greeting")
    
    # String with expiration
    redis_client.set_string("temp_key", "This will expire", expire_seconds=10)
    redis_client.get_string("temp_key")
    
    # JSON operations
    print("\n📦 JSON Operations:")
    user_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "skills": ["Python", "Redis", "Excel"]
    }
    redis_client.set_json("user:1", user_data)
    redis_client.get_json("user:1")
    
    # List operations
    print("\n📋 List Operations:")
    for task in ["Task 1", "Task 2", "Task 3"]:
        redis_client.add_to_list("todo_list", task)
    redis_client.get_list("todo_list")
    
    # Hash operations
    print("\n🏠 Hash Operations:")
    redis_client.set_hash("product:1", "name", "Laptop")
    redis_client.set_hash("product:1", "price", "999.99")
    redis_client.set_hash("product:1", "category", "Electronics")
    redis_client.get_hash("product:1")
    redis_client.get_hash("product:1", "name")
    
    # Key management
    print("\n🔑 Key Management:")
    redis_client.get_all_keys()
    
    # Cleanup
    print("\n🧹 Cleanup:")
    for key in ["greeting", "temp_key", "user:1", "todo_list", "product:1"]:
        redis_client.delete_key(key)


def demo_caching_pattern():
    """Demonstrate a simple caching pattern."""
    print("\n💾 Caching Pattern Demo")
    print("=" * 30)
    
    redis_client = RedisClient()
    
    if not redis_client.is_connected():
        return
    
    def expensive_computation(n):
        """Simulate an expensive computation."""
        print(f"🔄 Performing expensive computation for n={n}...")
        time.sleep(2)  # Simulate delay
        result = n ** 2 + n + 1
        return result
    
    def get_with_cache(n):
        """Get result with caching."""
        cache_key = f"computation:{n}"
        
        # Try to get from cache first
        cached_result = redis_client.get_string(cache_key)
        if cached_result:
            print(f"💨 Cache hit! Result: {cached_result}")
            return int(cached_result)
        
        # Cache miss - compute and store
        print("💾 Cache miss - computing...")
        result = expensive_computation(n)
        redis_client.set_string(cache_key, str(result), expire_seconds=60)
        return result
    
    # Demo caching
    test_values = [5, 3, 5, 3, 7]
    for value in test_values:
        print(f"\n📊 Getting result for {value}:")
        result = get_with_cache(value)
        print(f"Result: {result}")


if __name__ == "__main__":
    demo_basic_operations()
    demo_caching_pattern()
