"""
Redis and Excel integration examples.
Demonstrates combining Redis caching with Excel data processing.
"""
import json
import time
import os
from datetime import datetime, timedelta
import pandas as pd
from redis_examples import RedisClient
from excel_examples import ExcelProcessor
from config import DATA_DIR


class RedisExcelIntegration:
    """Combines Redis caching with Excel data processing."""
    
    def __init__(self):
        """Initialize Redis and Excel components."""
        self.redis_client = RedisClient()
        self.excel_processor = ExcelProcessor()
        print("🚀 Redis-Excel Integration initialized")
    
    def cache_excel_data(self, excel_file, sheet_name="Sheet1", cache_duration=300):
        """Load Excel data and cache it in Redis."""
        if not self.redis_client.is_connected():
            print("❌ Redis not connected")
            return False
        
        try:
            # Create cache key
            cache_key = f"excel_data:{os.path.basename(excel_file)}:{sheet_name}"
            
            # Check if already cached
            cached_data = self.redis_client.get_json(cache_key)
            if cached_data:
                print(f"💨 Data already cached for {excel_file}")
                return pd.DataFrame(cached_data)
            
            # Read Excel file
            print(f"📖 Reading Excel file: {excel_file}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            if df is None or df.empty:
                print("❌ No data found in Excel file")
                return None
            
            # Convert DataFrame to JSON-serializable format
            # Handle datetime objects by converting to string
            df_copy = df.copy()
            for col in df_copy.columns:
                if df_copy[col].dtype == 'datetime64[ns]':
                    df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            data_dict = df_copy.to_dict('records')
            
            # Cache the data
            success = self.redis_client.set_json(
                cache_key, 
                {
                    'data': data_dict,
                    'columns': list(df.columns),
                    'cached_at': datetime.now().isoformat(),
                    'row_count': len(df)
                },
                expire_seconds=cache_duration
            )
            
            if success:
                print(f"✅ Cached {len(df)} rows for {cache_duration} seconds")
                return df
            else:
                print("❌ Failed to cache data")
                return df
                
        except Exception as e:
            print(f"❌ Error caching Excel data: {e}")
            return None
    
    def get_cached_excel_data(self, excel_file, sheet_name="Sheet1"):
        """Retrieve cached Excel data from Redis."""
        if not self.redis_client.is_connected():
            print("❌ Redis not connected")
            return None
        
        try:
            cache_key = f"excel_data:{os.path.basename(excel_file)}:{sheet_name}"
            cached_data = self.redis_client.get_json(cache_key)
            
            if cached_data:
                df = pd.DataFrame(cached_data['data'])
                print(f"💨 Retrieved {cached_data['row_count']} rows from cache")
                print(f"📅 Cached at: {cached_data['cached_at']}")
                return df
            else:
                print("❌ No cached data found")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving cached data: {e}")
            return None
    
    def smart_excel_loader(self, excel_file, sheet_name="Sheet1", cache_duration=300):
        """Smart loader that tries cache first, then loads from file."""
        print(f"\n🧠 Smart loading: {excel_file}")
        
        # Try cache first
        df = self.get_cached_excel_data(excel_file, sheet_name)
        
        if df is not None:
            return df
        
        # Cache miss - load and cache
        print("🔄 Cache miss - loading from file...")
        df = self.cache_excel_data(excel_file, sheet_name, cache_duration)
        
        return df
    
    def process_and_cache_results(self, df, operation_name):
        """Process data and cache the results."""
        if df is None or not self.redis_client.is_connected():
            return None
        
        try:
            print(f"\n⚡ Processing operation: {operation_name}")
            
            # Different processing operations
            if operation_name == "department_summary":
                if 'Department' in df.columns and 'Salary' in df.columns:
                    result = df.groupby('Department').agg({
                        'Salary': ['mean', 'count', 'sum'],
                        'Age': 'mean'
                    }).round(2)
                    result.columns = ['Avg Salary', 'Count', 'Total Salary', 'Avg Age']
                    result = result.reset_index()
                else:
                    result = None
            
            elif operation_name == "age_groups":
                if 'Age' in df.columns:
                    df_copy = df.copy()
                    df_copy['Age Group'] = pd.cut(
                        df_copy['Age'], 
                        bins=[0, 25, 35, 50, 100], 
                        labels=['<25', '25-35', '35-50', '50+']
                    )
                    result = df_copy['Age Group'].value_counts().reset_index()
                    result.columns = ['Age Group', 'Count']
                else:
                    result = None
            
            elif operation_name == "high_performers":
                if 'Salary' in df.columns:
                    threshold = df['Salary'].quantile(0.75)  # Top 25%
                    result = df[df['Salary'] >= threshold].copy()
                else:
                    result = None
            
            else:
                print(f"❌ Unknown operation: {operation_name}")
                return None
            
            if result is None:
                print(f"❌ Could not perform operation: {operation_name}")
                return None
            
            # Cache the result
            cache_key = f"processed:{operation_name}:{datetime.now().strftime('%Y%m%d')}"
            
            if isinstance(result, pd.DataFrame):
                # Handle datetime columns in result DataFrame
                result_copy = result.copy()
                for col in result_copy.columns:
                    if result_copy[col].dtype == 'datetime64[ns]':
                        result_copy[col] = result_copy[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                result_dict = {
                    'data': result_copy.to_dict('records'),
                    'columns': list(result_copy.columns),
                    'operation': operation_name,
                    'processed_at': datetime.now().isoformat(),
                    'row_count': len(result_copy)
                }
            else:
                result_dict = {
                    'data': result,
                    'operation': operation_name,
                    'processed_at': datetime.now().isoformat()
                }
            
            success = self.redis_client.set_json(cache_key, result_dict, expire_seconds=3600)
            
            if success:
                print(f"✅ Cached processing result: {operation_name}")
                print(f"📊 Result:")
                if isinstance(result, pd.DataFrame):
                    print(result)
                else:
                    print(result)
                return result
            
        except Exception as e:
            print(f"❌ Error processing and caching: {e}")
            return None
    
    def get_processing_queue(self):
        """Demonstrate using Redis as a processing queue."""
        if not self.redis_client.is_connected():
            return
        
        print(f"\n🔄 Processing Queue Demo")
        print("=" * 30)
        
        queue_key = "excel_processing_queue"
        
        # Add some tasks to the queue
        tasks = [
            {"file": "sample_data.xlsx", "operation": "department_summary"},
            {"file": "sample_data.xlsx", "operation": "age_groups"},
            {"file": "sample_data.xlsx", "operation": "high_performers"}
        ]
        
        # Add tasks to queue
        for task in tasks:
            task_json = json.dumps(task)
            self.redis_client.add_to_list(queue_key, task_json)
            print(f"➕ Added task: {task}")
        
        # Process tasks from queue
        print(f"\n⚙️ Processing tasks from queue:")
        while True:
            # Get task from queue (FIFO)
            queue_items = self.redis_client.get_list(queue_key)
            if not queue_items:
                break
            
            # Remove and get the last item (FIFO behavior with lpush/rpop simulation)
            task_json = queue_items[-1]
            
            # Remove the task from queue
            self.redis_client.redis_client.lrem(queue_key, 1, task_json)
            
            try:
                task = json.loads(task_json)
                print(f"🔨 Processing: {task}")
                
                # Load data and process
                file_path = os.path.join(DATA_DIR, task['file'])
                if os.path.exists(file_path):
                    df = self.smart_excel_loader(file_path)
                    if df is not None:
                        self.process_and_cache_results(df, task['operation'])
                else:
                    print(f"❌ File not found: {file_path}")
                
                print("✅ Task completed\n")
                
            except Exception as e:
                print(f"❌ Error processing task: {e}")
    
    def cache_analytics(self):
        """Show cache analytics and statistics."""
        if not self.redis_client.is_connected():
            return
        
        print(f"\n📈 Cache Analytics")
        print("=" * 25)
        
        try:
            # Get all cache keys
            all_keys = self.redis_client.get_all_keys("*")
            if hasattr(all_keys, "__await__"):
                import asyncio
                all_keys = asyncio.run(all_keys)
            
            cache_stats = {
                'excel_data': 0,
                'processed': 0,
                'other': 0
            }
            
            for key in all_keys:
                if key.startswith('excel_data:'):
                    cache_stats['excel_data'] += 1
                elif key.startswith('processed:'):
                    cache_stats['processed'] += 1
                else:
                    cache_stats['other'] += 1
            
            print(f"📊 Cache Statistics:")
            print(f"  📁 Excel data caches: {cache_stats['excel_data']}")
            print(f"  ⚡ Processed results: {cache_stats['processed']}")
            print(f"  🔧 Other keys: {cache_stats['other']}")
            print(f"  📈 Total keys: {len(all_keys)}")
            
            # Show some cache details
            excel_keys = [k for k in all_keys if k.startswith('excel_data:')]
            if excel_keys:
                print(f"\n📁 Excel data caches:")
                for key in excel_keys[:5]:  # Show first 5
                    cached_info = self.redis_client.get_json(key)
                    if cached_info:
                        print(f"  {key}: {cached_info.get('row_count', 0)} rows, cached at {cached_info.get('cached_at', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Error getting cache analytics: {e}")


def demo_integration():
    """Main demo of Redis-Excel integration."""
    print("🔗 Redis-Excel Integration Demo")
    print("=" * 40)
    
    integration = RedisExcelIntegration()
    
    if not integration.redis_client.is_connected():
        print("❌ Cannot proceed without Redis connection")
        return
    
    # Create sample data first
    integration.excel_processor.create_sample_data()
    
    sample_file = os.path.join(DATA_DIR, 'sample_data.xlsx')
    
    # Demo 1: Smart loading with caching
    print("\n📋 Demo 1: Smart Excel Loading")
    df1 = integration.smart_excel_loader(sample_file, cache_duration=60)
    
    # Demo 2: Load again (should hit cache)
    print("\n📋 Demo 2: Loading Again (Cache Hit)")
    df2 = integration.smart_excel_loader(sample_file)
    
    # Demo 3: Process and cache results
    if df1 is not None:
        print("\n📋 Demo 3: Processing and Caching Results")
        integration.process_and_cache_results(df1, "department_summary")
        integration.process_and_cache_results(df1, "age_groups")
        integration.process_and_cache_results(df1, "high_performers")
    
    # Demo 4: Processing queue
    print("\n📋 Demo 4: Processing Queue")
    integration.get_processing_queue()
    
    # Demo 5: Cache analytics
    print("\n📋 Demo 5: Cache Analytics")
    integration.cache_analytics()


def demo_performance_comparison():
    """Compare performance with and without Redis caching."""
    print("\n⚡ Performance Comparison Demo")
    print("=" * 35)
    
    integration = RedisExcelIntegration()
    
    if not integration.redis_client.is_connected():
        print("❌ Cannot proceed without Redis connection")
        return
    
    sample_file = os.path.join(DATA_DIR, 'sample_data.xlsx')
    
    # Clear any existing cache
    cache_key = f"excel_data:{os.path.basename(sample_file)}:Sheet1"
    integration.redis_client.delete_key(cache_key)
    
    # Time without cache (first load)
    print("🕐 Loading without cache...")
    start_time = time.time()
    df1 = integration.smart_excel_loader(sample_file)
    first_load_time = time.time() - start_time
    print(f"⏱️ First load time: {first_load_time:.3f} seconds")
    
    # Time with cache (second load)
    print("\n🕐 Loading with cache...")
    start_time = time.time()
    df2 = integration.smart_excel_loader(sample_file)
    cached_load_time = time.time() - start_time
    print(f"⏱️ Cached load time: {cached_load_time:.3f} seconds")
    
    if first_load_time > 0:
        speedup = first_load_time / cached_load_time if cached_load_time > 0 else float('inf')
        print(f"🚀 Speedup: {speedup:.1f}x faster with cache!")


if __name__ == "__main__":
    demo_integration()
    demo_performance_comparison()
