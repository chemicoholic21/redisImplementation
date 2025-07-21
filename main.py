"""
Main entry point for Redis Excel Integration demonstrations.
Run this file to see all examples in action.
"""
import sys
import os

def show_menu():
    """Display the main menu options."""
    print("\n🚀 Redis Excel Integration Examples")
    print("=" * 40)
    print("1. 📊 Excel Operations Demo")
    print("2. 🔗 Redis Operations Demo")
    print("3. ⚡ Redis-Excel Integration Demo")
    print("4. 📈 Performance Comparison")
    print("5. ❓ Help & Setup Instructions")
    print("0. 🚪 Exit")
    print("=" * 40)

def show_help():
    """Display help and setup instructions."""
    print("\n❓ Help & Setup Instructions")
    print("=" * 35)
    print("📋 Prerequisites:")
    print("  • Python 3.7+ with virtual environment activated")
    print("  • Redis server running (localhost:6379)")
    print("  • Required packages installed (see requirements.txt)")
    print("\n🔧 Setup Steps:")
    print("  1. Install Redis server:")
    print("     • Windows: Download from https://redis.io/download")
    print("     • Or use Docker: docker run -d -p 6379:6379 redis:alpine")
    print("  2. Start Redis server:")
    print("     • Windows: redis-server.exe")
    print("     • Docker: redis container should start automatically")
    print("  3. Install Python packages:")
    print("     • pip install -r requirements.txt")
    print("\n📁 Project Structure:")
    print("  • src/redis_examples.py - Basic Redis operations")
    print("  • src/excel_examples.py - Excel file processing")
    print("  • src/redis_excel_integration.py - Combined examples")
    print("  • data/ - Sample data files")
    print("\n💡 Tips:")
    print("  • Excel examples work without Redis")
    print("  • Redis examples require running Redis server")
    print("  • Integration examples need both Excel data and Redis")

def run_excel_demo():
    """Run Excel operations demo."""
    try:
        print("\n🎬 Starting Excel Operations Demo...")
        import sys
        sys.path.append('src')
        from excel_examples import demo_excel_operations, demo_multiple_sheets
        demo_excel_operations()
        demo_multiple_sheets()
        print("\n✅ Excel demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error running Excel demo: {e}")
        print("💡 Make sure all required packages are installed.")

def run_redis_demo():
    """Run Redis operations demo."""
    try:
        print("\n🎬 Starting Redis Operations Demo...")
        import sys
        sys.path.append('src')
        from redis_examples import demo_basic_operations, demo_caching_pattern
        demo_basic_operations()
        demo_caching_pattern()
        print("\n✅ Redis demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error running Redis demo: {e}")
        print("💡 Make sure Redis server is running and accessible.")

def run_integration_demo():
    """Run Redis-Excel integration demo."""
    try:
        print("\n🎬 Starting Redis-Excel Integration Demo...")
        import sys
        sys.path.append('src')
        from redis_excel_integration import demo_integration
        demo_integration()
        print("\n✅ Integration demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error running integration demo: {e}")
        print("💡 Make sure both Redis server is running and Excel files are accessible.")

def run_performance_demo():
    """Run performance comparison demo."""
    try:
        print("\n🎬 Starting Performance Comparison Demo...")
        import sys
        sys.path.append('src')
        from redis_excel_integration import demo_performance_comparison
        demo_performance_comparison()
        print("\n✅ Performance demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error running performance demo: {e}")
        print("💡 Make sure Redis server is running.")

def main():
    """Main application loop."""
    while True:
        try:
            show_menu()
            choice = input("\n🎯 Select an option (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for using Redis Excel Integration!")
                print("Happy coding! 🚀")
                sys.exit(0)
            
            elif choice == '1':
                run_excel_demo()
            
            elif choice == '2':
                run_redis_demo()
            
            elif choice == '3':
                run_integration_demo()
            
            elif choice == '4':
                run_performance_demo()
            
            elif choice == '5':
                show_help()
            
            else:
                print("\n❌ Invalid option. Please select 0-5.")
            
            input("\n⏸️ Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    print("🎉 Welcome to Redis Excel Integration Examples!")
    print("This project demonstrates combining Redis caching with Excel data processing.")
    main()
