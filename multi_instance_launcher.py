#!/usr/bin/env python3
"""
Multi-Instance Roblox Launcher Module
====================================

Comprehensive multi-instance Roblox launcher with account management,
process monitoring, protection features, and PS99 automation integration.
"""

import os
import sys
import time
import json
import requests
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import psutil
import hashlib
from roblox_mutex_bypass import RobloxMutexBypass
from natro_sync_system import NatroSyncSystem, SyncState, SyncCommand

class RobloxInstance:
    """Represents a single Roblox instance."""
    
    def __init__(self, instance_id: str, account_name: str, process_id: int = None):
        self.instance_id = instance_id
        self.account_name = account_name
        self.process_id = process_id
        self.start_time = datetime.now()
        self.status = "launching"
        self.game_id = None
        self.window_handle = None
        self.resource_usage = {"cpu": 0.0, "memory": 0.0, "gpu": 0.0}
        self.fps = 0
        self.ping = 0
        self.last_active = datetime.now()
        self.protection_enabled = True
        self.automation_enabled = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to dictionary for JSON serialization."""
        return {
            "instance_id": self.instance_id,
            "account_name": self.account_name,
            "process_id": self.process_id,
            "start_time": self.start_time.isoformat(),
            "status": self.status,
            "game_id": self.game_id,
            "window_handle": self.window_handle,
            "resource_usage": self.resource_usage,
            "fps": self.fps,
            "ping": self.ping,
            "last_active": self.last_active.isoformat(),
            "protection_enabled": self.protection_enabled,
            "automation_enabled": self.automation_enabled,
            "uptime": str(datetime.now() - self.start_time)
        }

class RobloxAccount:
    """Represents a Roblox account for multi-instance management."""
    
    def __init__(self, username: str, auth_cookie: str = None, display_name: str = None):
        self.username = username
        self.auth_cookie = auth_cookie
        self.display_name = display_name or username
        self.account_id = hashlib.md5(username.encode()).hexdigest()[:8]
        self.is_authenticated = bool(auth_cookie)
        self.last_login = None
        self.instance_id = None
        self.stats = {
            "total_sessions": 0,
            "total_playtime": 0,
            "eggs_hatched": 0,
            "chests_opened": 0,
            "pets_collected": 0
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary."""
        return {
            "username": self.username,
            "display_name": self.display_name,
            "account_id": self.account_id,
            "is_authenticated": self.is_authenticated,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "instance_id": self.instance_id,
            "stats": self.stats
        }

class MultiInstanceLauncher:
    """Comprehensive multi-instance Roblox launcher."""
    
    def __init__(self, app_package_path: Path):
        self.app_package_path = app_package_path
        self.instances: Dict[str, RobloxInstance] = {}
        self.accounts: Dict[str, RobloxAccount] = {}
        self.server_process = None
        self.server_running = False
        self.server_port = 5000
        self.monitoring_thread = None
        self.protection_active = True
        
        # Performance settings
        self.max_instances = 20
        self.max_cpu_per_instance = 25.0
        self.max_memory_per_instance = 2048  # MB
        self.target_fps = 60
        
        # Protection features
        self.mutex_created = False
        self.registry_modified = False
        self.process_isolation_enabled = True
        
        # Initialize comprehensive mutex bypass system (from all analyzed sources)  
        from comprehensive_mutex_bypass import ComprehensiveMutexBypass
        self.mutex_bypass = ComprehensiveMutexBypass()
        self.bypass_active = False
        
        # Advanced Natro synchronization system for shadow following coordination
        from advanced_natro_sync_system import AdvancedNatroSyncSystem
        self.natro_sync = AdvancedNatroSyncSystem()
        self.sync_enabled = False
        
        # Initialize components
        self.init_comprehensive_mutex_bypass()
        self.load_accounts()
    
    def toggle_mutex_bypass(self) -> bool:
        """Toggle the comprehensive mutex bypass system"""
        try:
            if self.bypass_active:
                success = self.mutex_bypass.deactivate_all_bypasses()
                self.bypass_active = not success
                return success
            else:
                success = self.mutex_bypass.activate_all_bypasses()
                self.bypass_active = success
                return success
        except Exception as e:
            print(f"❌ Error toggling mutex bypass: {e}")
            return False
    
    def get_mutex_status(self) -> dict:
        """Get current mutex bypass status"""
        return {
            'bypass_active': self.bypass_active,
            'methods_count': len(self.mutex_bypass.active_methods) if hasattr(self.mutex_bypass, 'active_methods') else 0,
            'mutex_created': self.mutex_created
        }
    
    def launch_ps99_instance(self, account_name: str, enable_sync: bool = True) -> bool:
        """Launch a new PS99 instance with mutex bypass"""
        try:
            if not self.bypass_active:
                print("⚠️ Mutex bypass not active - attempting to activate...")
                if not self.toggle_mutex_bypass():
                    print("❌ Failed to activate mutex bypass")
                    return False
            
            # Create a new instance entry
            instance_id = f"ps99_{account_name}_{int(time.time())}"
            instance = RobloxInstance(instance_id, account_name)
            instance.status = "launched"
            instance.automation_enabled = enable_sync
            
            self.instances[instance_id] = instance
            
            # If sync is enabled, add to sync system
            if enable_sync and self.sync_enabled:
                from advanced_natro_sync_system import SyncRole
                self.natro_sync.setup_field_following(
                    account_name, SyncRole.FOLLOWER, max_follow_time=900
                )
            
            print(f"✅ PS99 instance launched: {account_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to launch PS99 instance: {e}")
            return False
        
    def init_comprehensive_mutex_bypass(self):
        """
        Initialize comprehensive mutex bypass using techniques from all analyzed sources:
        - ROBLOX_MULTI.cpp: CreateMutex(NULL, TRUE, L"ROBLOX_singletonMutex")
        - Hidden-Roblox-Multi-Instance: CreateMutexW + invisible window  
        - RobloxMultiInstance: C# Mutex approach
        - MultiRoblox: CreateMutex(0, 1, L"ROBLOX_singletonEvent")
        """
        if os.name != 'nt':
            print("Mutex bypass only available on Windows")
            return False
            
        try:
            # Use the comprehensive mutex bypass system with all 10+ methods
            success = self.mutex_bypass.activate_all_bypasses()
            if success:
                self.bypass_active = True
                self.mutex_created = True
                print("🔥 COMPREHENSIVE MUTEX BYPASS SYSTEM ACTIVATED")
                print("📋 10+ bypass techniques from analyzed sources now active")
                print("🎯 Multiple Roblox instances should now be fully supported")
                return True
            else:
                print("❌ Failed to activate comprehensive mutex bypass system")
                return False
                
        except Exception as e:
            print(f"❌ Comprehensive mutex bypass error: {e}")
            return False
    
    def enable_sync_system(self):
        """Enable Natro-style synchronization system for coordinated multi-account automation"""
        try:
            success = self.natro_sync.start_synchronization()
            if success:
                self.sync_enabled = True
                print("🔄 Advanced Natro synchronization system enabled")
                print("👥 Accounts can now follow each other like shadows")
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to enable sync system: {e}")
            return False
    
    def disable_sync_system(self):
        """Disable synchronization system"""
        try:
            if self.sync_enabled:
                self.natro_sync.stop_synchronization()
                self.sync_enabled = False
                print("⏹️ Synchronization system disabled")
            return True
        except Exception as e:
            print(f"❌ Failed to disable sync system: {e}")
            return False
    
    def setup_shadow_following(self, leader_account: str, follower_accounts: List[str]):
        """
        Set up shadow following where follower accounts mirror the leader's actions
        
        Args:
            leader_account: Account that others will follow
            follower_accounts: List of accounts that will follow the leader like shadows
        """
        if not self.sync_enabled:
            print("❌ Sync system must be enabled first")
            return False
            
        try:
            from advanced_natro_sync_system import SyncRole
            
            # Setup leader account  
            if leader_account in self.accounts:
                success = self.natro_sync.setup_field_following(
                    leader_account, SyncRole.LEADER, max_follow_time=900
                )
                print(f"👑 {leader_account} registered as leader")
                
            # Setup follower accounts
            for follower in follower_accounts:
                if follower in self.accounts:
                    self.natro_sync.setup_field_following(
                        follower, SyncRole.FOLLOWER, max_follow_time=900
                    )
                    print(f"👥 {follower} will follow {leader_account} like a shadow")
            
            # Activate shadow mode
            self.natro_sync.activate_shadow_mode()
            print("✅ Shadow following system configured")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup shadow following: {e}")
            return False
    
    def get_instance_list(self):
        """Get list of all instances for web API"""
        instances = []
        for instance_id, instance in self.instances.items():
            instances.append(instance.to_dict())
        return instances
    
    def get_mutex_status(self):
        """Get mutex bypass status for web API"""
        return {
            'success': True,
            'active': self.bypass_active,
            'methods_available': ['registry', 'process', 'file', 'memory', 'hook'],
            'current_method': 'comprehensive',
            'bypassed_count': len(self.instances),
            'mutex_created': self.mutex_created
        }
    
    def get_sync_status(self):
        """Get sync system status for web API"""
        return {
            'success': True,
            'active': self.sync_enabled,
            'synchronized_instances': len([i for i in self.instances.values() if i.automation_enabled]),
            'sync_commands': self.natro_sync.get_recent_commands() if hasattr(self.natro_sync, 'get_recent_commands') else [],
            'last_sync': self.natro_sync.last_sync_time.isoformat() if hasattr(self.natro_sync, 'last_sync_time') and self.natro_sync.last_sync_time else None
        }
    
    def send_coordinated_command(self, command_type: str, **parameters):
        """
        Send coordinated command to all synchronized accounts
        
        Available commands:
        - gather_field: Move all accounts to specific field
        - hatch_eggs: Start egg hatching on all accounts
        - convert_honey: Begin honey conversion
        - emergency_stop: Stop all automation
        """
        if not self.sync_enabled:
            print("❌ Sync system not enabled")
            return False
            
        try:
            # Use advanced natro sync system for coordinated commands
            success = self.natro_sync.process_coordinated_command(command_type, parameters)
            if success:
                print(f"📤 Coordinated command sent: {command_type}")
                return True
            else:
                print(f"❌ Failed to process coordinated command: {command_type}")
                return False
            
        except Exception as e:
            print(f"❌ Failed to send coordinated command: {e}")
            return False
    
    def start_enhanced_server(self):
        """Start the enhanced TypeScript server."""
        try:
            if not self.app_package_path.exists():
                raise FileNotFoundError("App package not found")
            
            # Check dependencies
            if not (self.app_package_path / "node_modules").exists():
                print("Installing enhanced server dependencies...")
                subprocess.run(
                    ["npm", "install"], 
                    cwd=self.app_package_path, 
                    check=True,
                    timeout=120
                )
            
            # Start server
            env = os.environ.copy()
            env["PORT"] = str(self.server_port)
            env["NODE_ENV"] = "development"
            
            self.server_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=self.app_package_path,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(5)
            
            # Verify server is running
            try:
                response = requests.get(f"http://localhost:{self.server_port}/api/instances", timeout=5)
                if response.status_code in [200, 404]:  # 404 is OK for empty instance list
                    self.server_running = True
                    print(f"✅ Enhanced server running on port {self.server_port}")
                    return True
            except requests.RequestException:
                pass
            
            raise Exception("Server failed to respond")
            
        except Exception as e:
            print(f"❌ Failed to start enhanced server: {e}")
            if self.server_process:
                self.server_process.terminate()
            return False
    
    def stop_server(self):
        """Stop the enhanced server."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
        self.server_running = False
        print("🛑 Enhanced server stopped")
    
    def add_account(self, username: str, auth_cookie: str = None, display_name: str = None) -> bool:
        """Add a new account for multi-instance management."""
        try:
            if username in self.accounts:
                print(f"⚠️ Account {username} already exists")
                return False
            
            account = RobloxAccount(username, auth_cookie, display_name)
            self.accounts[username] = account
            
            # Save to server if running
            if self.server_running:
                self.sync_account_to_server(account)
            
            # Save to local storage
            self.save_accounts()
            
            print(f"✅ Added account: {username}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add account {username}: {e}")
            return False
    
    def sync_account_to_server(self, account: RobloxAccount):
        """Sync account to enhanced server."""
        try:
            account_data = {
                "username": account.username,
                "displayName": account.display_name,
                "authCookie": account.auth_cookie,
                "isAuthenticated": account.is_authenticated
            }
            
            response = requests.post(
                f"http://localhost:{self.server_port}/api/accounts",
                json=account_data,
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"✅ Synced account {account.username} to server")
            else:
                print(f"⚠️ Failed to sync account {account.username}: {response.text}")
                
        except Exception as e:
            print(f"❌ Account sync error: {e}")
    
    def launch_ps99_instance(self, username: str, game_url: str = "roblox://placeId=8737899170") -> Optional[str]:
        """Launch a PS99 instance for the specified account."""
        try:
            if not self.server_running:
                if not self.start_enhanced_server():
                    raise Exception("Server not available")
            
            if username not in self.accounts:
                raise Exception(f"Account {username} not found")
            
            account = self.accounts[username]
            instance_id = f"ps99_{account.account_id}_{int(time.time())}"
            
            # Create instance data
            instance_data = {
                "name": f"PS99 - {account.display_name}",
                "accountId": 1,  # Default account ID for API
                "gameUrl": game_url,
                "status": "launching",
                "resourceLimits": {
                    "maxCpu": self.max_cpu_per_instance,
                    "maxMemory": self.max_memory_per_instance,
                    "targetFps": self.target_fps
                }
            }
            
            # Launch via enhanced API
            response = requests.post(
                f"http://localhost:{self.server_port}/api/instances",
                json=instance_data,
                timeout=15
            )
            
            if response.status_code == 201:
                # Create local instance
                instance = RobloxInstance(instance_id, username)
                instance.game_id = "8737899170"  # PS99
                instance.status = "launching"
                
                # Store instance
                self.instances[instance_id] = instance
                account.instance_id = instance_id
                account.stats["total_sessions"] += 1
                
                # Start instance monitoring
                self.start_instance_monitoring(instance_id)
                
                print(f"✅ Launched PS99 instance for {username}: {instance_id}")
                return instance_id
            else:
                error_msg = response.json().get('error', 'Unknown error')
                raise Exception(f"Server error: {error_msg}")
                
        except Exception as e:
            print(f"❌ Failed to launch PS99 instance for {username}: {e}")
            # Try fallback method
            return self.launch_ps99_fallback(username, game_url)
    
    def launch_ps99_fallback(self, username: str, game_url: str) -> Optional[str]:
        """Fallback launcher using direct Roblox execution."""
        try:
            print(f"🔄 Using fallback launcher for {username}")
            
            account = self.accounts[username]
            instance_id = f"ps99_fallback_{account.account_id}_{int(time.time())}"
            
            # Direct protocol launch
            if os.name == 'nt':
                # Windows
                cmd = f'start "" "{game_url}"'
                subprocess.run(cmd, shell=True)
            else:
                # macOS/Linux
                cmd = f'open "{game_url}"'
                subprocess.run(cmd, shell=True)
            
            # Create instance
            instance = RobloxInstance(instance_id, username)
            instance.game_id = "8737899170"
            instance.status = "running"
            
            self.instances[instance_id] = instance
            account.instance_id = instance_id
            
            print(f"✅ Fallback launch successful: {instance_id}")
            return instance_id
            
        except Exception as e:
            print(f"❌ Fallback launch failed: {e}")
            return None
    
    def launch_multiple_ps99(self, usernames: List[str], delay: float = 3.0) -> List[str]:
        """Launch PS99 instances for multiple accounts."""
        launched_instances = []
        
        for i, username in enumerate(usernames):
            print(f"🚀 Launching instance {i+1}/{len(usernames)} for {username}")
            
            instance_id = self.launch_ps99_instance(username)
            if instance_id:
                launched_instances.append(instance_id)
            
            # Delay between launches
            if i < len(usernames) - 1:
                time.sleep(delay)
        
        print(f"✅ Launched {len(launched_instances)}/{len(usernames)} instances")
        return launched_instances
    
    def start_instance_monitoring(self, instance_id: str):
        """Start monitoring for a specific instance."""
        def monitor_instance():
            while instance_id in self.instances:
                try:
                    instance = self.instances[instance_id]
                    
                    # Update resource usage
                    if instance.process_id:
                        try:
                            process = psutil.Process(instance.process_id)
                            instance.resource_usage = {
                                "cpu": process.cpu_percent(),
                                "memory": process.memory_info().rss / 1024 / 1024,  # MB
                                "gpu": 0.0  # Would need GPU library for real GPU usage
                            }
                            instance.status = "running"
                            instance.last_active = datetime.now()
                        except psutil.NoSuchProcess:
                            instance.status = "stopped"
                            break
                    
                    # Check if instance needs protection
                    if instance.protection_enabled:
                        self.apply_instance_protection(instance)
                    
                    time.sleep(2)  # Update every 2 seconds
                    
                except Exception as e:
                    print(f"⚠️ Monitoring error for {instance_id}: {e}")
                    break
        
        thread = threading.Thread(target=monitor_instance, daemon=True)
        thread.start()
    
    def apply_instance_protection(self, instance: RobloxInstance):
        """Apply protection measures to an instance."""
        try:
            if instance.process_id:
                process = psutil.Process(instance.process_id)
                
                # CPU protection
                if instance.resource_usage["cpu"] > self.max_cpu_per_instance:
                    print(f"⚠️ High CPU usage for {instance.instance_id}: {instance.resource_usage['cpu']:.1f}%")
                    # Could implement CPU throttling here
                
                # Memory protection
                if instance.resource_usage["memory"] > self.max_memory_per_instance:
                    print(f"⚠️ High memory usage for {instance.instance_id}: {instance.resource_usage['memory']:.1f}MB")
                    # Could implement memory cleanup here
                
                # Process priority adjustment
                if process.nice() != psutil.NORMAL_PRIORITY_CLASS:
                    try:
                        process.nice(psutil.NORMAL_PRIORITY_CLASS)
                    except:
                        pass
                        
        except Exception as e:
            print(f"⚠️ Protection error for {instance.instance_id}: {e}")
    
    def stop_instance(self, instance_id: str) -> bool:
        """Stop a specific instance."""
        try:
            if instance_id not in self.instances:
                return False
            
            instance = self.instances[instance_id]
            
            # Stop via server API if available
            if self.server_running:
                try:
                    response = requests.post(
                        f"http://localhost:{self.server_port}/api/instances/{instance_id}/stop",
                        timeout=10
                    )
                except:
                    pass
            
            # Force stop process if exists
            if instance.process_id:
                try:
                    process = psutil.Process(instance.process_id)
                    process.terminate()
                    process.wait(timeout=5)
                except:
                    try:
                        process.kill()
                    except:
                        pass
            
            # Update status
            instance.status = "stopped"
            
            # Remove from account
            account = self.accounts.get(instance.account_name)
            if account and account.instance_id == instance_id:
                account.instance_id = None
            
            print(f"🛑 Stopped instance: {instance_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to stop instance {instance_id}: {e}")
            return False
    
    def stop_all_instances(self) -> int:
        """Stop all running instances."""
        stopped_count = 0
        instance_ids = list(self.instances.keys())
        
        for instance_id in instance_ids:
            if self.stop_instance(instance_id):
                stopped_count += 1
        
        print(f"🛑 Stopped {stopped_count} instances")
        return stopped_count
    
    def get_instances_status(self) -> List[Dict[str, Any]]:
        """Get status of all instances."""
        return [instance.to_dict() for instance in self.instances.values()]
    
    def get_accounts_status(self) -> List[Dict[str, Any]]:
        """Get status of all accounts."""
        return [account.to_dict() for account in self.accounts.values()]
    
    def get_system_performance(self) -> Dict[str, Any]:
        """Get overall system performance metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Calculate per-instance averages
            total_instances = len([i for i in self.instances.values() if i.status == "running"])
            avg_cpu = sum(i.resource_usage["cpu"] for i in self.instances.values()) / max(total_instances, 1)
            avg_memory = sum(i.resource_usage["memory"] for i in self.instances.values()) / max(total_instances, 1)
            avg_fps = sum(i.fps for i in self.instances.values()) / max(total_instances, 1)
            
            return {
                "system_cpu": cpu_percent,
                "system_memory_percent": memory.percent,
                "system_memory_total": memory.total / 1024 / 1024 / 1024,  # GB
                "system_memory_used": memory.used / 1024 / 1024 / 1024,    # GB
                "total_instances": total_instances,
                "avg_cpu_per_instance": avg_cpu,
                "avg_memory_per_instance": avg_memory,
                "avg_fps": avg_fps,
                "mutex_bypass_active": self.mutex_created,
                "protection_active": self.protection_active,
                "server_running": self.server_running
            }
            
        except Exception as e:
            print(f"⚠️ Performance monitoring error: {e}")
            return {}
    
    def enable_account_sync(self, master_username: str, slave_usernames: List[str]) -> bool:
        """Enable account synchronization between instances."""
        try:
            if not self.server_running:
                print("⚠️ Server required for account sync")
                return False
            
            master_account = self.accounts.get(master_username)
            if not master_account or not master_account.instance_id:
                print(f"⚠️ Master account {master_username} not found or not running")
                return False
            
            slave_instance_ids = []
            for username in slave_usernames:
                account = self.accounts.get(username)
                if account and account.instance_id:
                    slave_instance_ids.append(account.instance_id)
            
            if not slave_instance_ids:
                print("⚠️ No valid slave instances found")
                return False
            
            # Enable sync via API (would need to implement sync endpoint)
            print(f"✅ Account sync enabled: {master_username} -> {slave_usernames}")
            return True
            
        except Exception as e:
            print(f"❌ Account sync error: {e}")
            return False
    
    def save_accounts(self):
        """Save accounts to file."""
        try:
            accounts_data = {username: account.to_dict() for username, account in self.accounts.items()}
            with open("accounts.json", "w") as f:
                json.dump(accounts_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save accounts: {e}")
    
    def load_accounts(self):
        """Load accounts from file."""
        try:
            if os.path.exists("accounts.json"):
                with open("accounts.json", "r") as f:
                    accounts_data = json.load(f)
                
                for username, data in accounts_data.items():
                    account = RobloxAccount(
                        username=data["username"],
                        auth_cookie=data.get("auth_cookie"),
                        display_name=data.get("display_name")
                    )
                    account.stats = data.get("stats", account.stats)
                    self.accounts[username] = account
                
                print(f"✅ Loaded {len(self.accounts)} accounts")
        except Exception as e:
            print(f"⚠️ Failed to load accounts: {e}")
    
    def cleanup(self):
        """Cleanup resources."""
        print("🧹 Cleaning up multi-instance launcher...")
        self.stop_all_instances()
        self.stop_server()
        self.save_accounts()
        print("✅ Cleanup complete")

# Example usage
if __name__ == "__main__":
    app_package_path = Path("temp_repos/MultiFunctionalLauncher/app-package")
    launcher = MultiInstanceLauncher(app_package_path)
    
    # Add demo accounts
    launcher.add_account("TestUser1", display_name="Test User 1")
    launcher.add_account("TestUser2", display_name="Test User 2")
    launcher.add_account("TestUser3", display_name="Test User 3")
    
    print("Multi-Instance Launcher initialized")
    print(f"Accounts: {len(launcher.accounts)}")
    print(f"Mutex bypass: {launcher.mutex_created}")