# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\_gateway.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 9603 bytes
import threading
from py4j.java_gateway import JavaGateway, CallbackServerParameters, GatewayParameters
from ._logger import log_info, log_warning
import subprocess, os, select, socket, platform, time

def _get_jar_file():
    jar_path = _get_jar_dir()
    jar_name = "original-iobjects-py4j.jar"
    jar_file = "%s/%s" % (jar_path, jar_name)
    if not os.path.exists(jar_file):
        jar_name = "iobjects-py4j.jar"
        return "%s/%s" % (jar_path, jar_name)
    return jar_file


def _get_jar_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "jars")


class _JavaHeartBeatThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.socket_heart = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_heart.bind(('127.0.0.1', 0))
        self.socket_heart.listen(1)
        self.host, self.port = self.socket_heart.getsockname()

    def run(self):
        self.socket_heart.listen(1)
        try:
            try:
                conn, _ = self.socket_heart.accept()
                pid = os.getpid()
                send_data = str(pid).encode("utf-8")
                while True:
                    time.sleep(1)
                    conn.send(send_data)
                    rev_data = conn.recv(128)
                    if not rev_data:
                        time.sleep(0.1)
                        continue
                    conn.send(send_data)

                conn.close()
            except Exception:
                pass

        finally:
            self.socket_heart.close()


class _JavaGatewayLaunchThread(threading.Thread):

    def __init__(self, callback_host, callback_port):
        threading.Thread.__init__(self)
        self.callback_host = callback_host
        self.callback_port = callback_port

    def run(self):
        jar_file = _get_jar_file()
        sysstr = platform.system()
        from . import get_iobjects_java_path
        java_bin_path = get_iobjects_java_path()
        if sysstr == "Windows":
            comment = 'start /b java -cp "%s" com.supermap.jsuperpy.ApplicationExample %s %s' % (
             jar_file, self.callback_host, self.callback_port)
            print(comment)
            env = os.environ
            if java_bin_path is not None:
                try:
                    env["PATH"] = java_bin_path + ";" + env["PATH"]
                except:
                    log_warning("failed set iobjects-java-bin to PATH")

            subprocess.Popen(comment, shell=True, start_new_session=True, env=env)
        else:
            if sysstr == "Linux":
                comment = "java -cp %s com.supermap.jsuperpy.ApplicationExample %s %s" % (
                 jar_file, self.callback_host, self.callback_port)
                print(comment)
                env = os.environ
                if java_bin_path is not None:
                    try:
                        env["PATH"] = java_bin_path + ":" + env["PATH"]
                    except:
                        log_warning("failed set iobjects-java-bin to PATH")

                    try:
                        env["LD_LIBRARY_PATH"] = java_bin_path + ":" + env["LD_LIBRARY_PATH"]
                    except:
                        log_warning("failed set iobjects-java-bin to LD_LIBRARY_PATH")

                subprocess.Popen(comment, shell=True, start_new_session=True, env=env)
            else:
                raise RuntimeError("Unsupported system : " + sysstr)


class _GatewayManager(object):

    def __init__(self):
        self._gateway = None
        self._port = 0
        self.lock = threading.Lock()
        self.is_desktop_mode = False
        self.is_outer_gateway = False

    def set_port(self, port):
        if port > 0:
            self.is_desktop_mode = True
            self.is_outer_gateway = True
            self._port = port

    def shutdown(self):
        if not self.is_desktop_mode:
            if not self.is_outer_gateway:
                self.lock.acquire()
                from .data import Workspace
                Workspace.close()
                if self._gateway is not None:
                    self._gateway.shutdown()
                    print("[iObjectsPy]: Gateway-service closed successfully")
                    self._gateway = None
                else:
                    log_info("[iObjectsPy]: No gateway server running")
                self.lock.release()

    @staticmethod
    def connect_gateway(gateway_port):
        _gateway = JavaGateway(gateway_parameters=GatewayParameters(port=gateway_port, auto_convert=True))
        pnt = _gateway.jvm.com.supermap.data.Point2D()
        del pnt
        _gateway.start_callback_server(CallbackServerParameters(port=0, eager_load=True, daemonize=True))
        return _gateway

    @staticmethod
    def read_int(stream):
        length = stream.read(4)
        if not length:
            raise EOFError
        import struct
        return struct.unpack("!i", length)[0]

    def launch_gateway(self):
        _gateway = None
        try:
            if not self.is_desktop_mode:
                callback_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                callback_socket.bind(('127.0.0.1', 0))
                callback_socket.listen(1)
                callback_host, callback_port = callback_socket.getsockname()
                java_server_launch = _JavaGatewayLaunchThread(callback_host, str(callback_port))
                java_server_launch.start()
                gateway_port = None
                while gateway_port is None:
                    timeout = 1
                    readable, _, _ = select.select([callback_socket], [], [], timeout)
                    if callback_socket in readable:
                        gateway_connection = callback_socket.accept()[0]
                        gateway_port = _GatewayManager.read_int(gateway_connection.makefile(mode="rb"))
                        gateway_connection.close()

                callback_socket.close()
                self._port = gateway_port
            else:
                count = 0
                while _gateway is None and count < 10:
                    count += 1
                    time.sleep(0.1)
                    try:
                        _gateway = _GatewayManager.connect_gateway(self._port)
                    except:
                        import traceback
                        traceback.print_exc()
                        _gateway = None

                if _gateway is not None and _gateway.get_callback_server() is not None:
                    python_proxy_address = _gateway.get_callback_server().get_listening_address()
                    python_proxy_port = _gateway.get_callback_server().get_listening_port()
                    _gateway.entry_point.resetPythonPort(python_proxy_address, python_proxy_port)
                    print("[iObjectsPy]: Connection gateway-service successful, Python callback port bind " + str(python_proxy_port))
                    print()
                    heart_beat_server = self.is_desktop_mode or _JavaHeartBeatThread()
                    heart_beat_server.setDaemon(True)
                    heart_beat_server.start()
                    _gateway.entry_point.startHeartBeatClient(heart_beat_server.host, heart_beat_server.port)
                else:
                    raise RuntimeError("[iObjectsPy]: Failed to connect java Gateway")
        except:
            import traceback
            traceback.print_exc()

        return _gateway

    @property
    def gateway(self):
        if self._gateway is None:
            self.lock.acquire()
            self._gateway = self.launch_gateway()
            self.lock.release()
            from .env import Env
            Env._set_all_to_java()
        return self._gateway

    def set_gateway(self, gt):
        if self._gateway is None:
            if gt is not None:
                self.lock.acquire()
                self._gateway = gt
                self.is_outer_gateway = True
                self.lock.release()
                from .env import Env
                Env._set_all_to_java()

    def close_callback_server(self):
        pass

    def safe_start_callback_server(self):
        return self.gateway.get_callback_server() is not None


_g_gateway_manager = _GatewayManager()

def set_gateway_port(port):
    _g_gateway_manager.set_port(port)


def get_gateway():
    return _g_gateway_manager.gateway


def set_gateway(gateway, func_load_jar):
    _g_gateway_manager.set_gateway(gateway)
    if func_load_jar is not None:
        func_load_jar(_get_jar_file())


def get_jvm():
    return _g_gateway_manager.gateway.jvm


def safe_start_callback_server():
    return _g_gateway_manager.safe_start_callback_server()


def close_callback_server():
    return _g_gateway_manager.close_callback_server()


def gateway_shutdown():
    _g_gateway_manager.shutdown()
