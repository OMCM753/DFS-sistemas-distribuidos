import socket, json, threading 

METADATA_DB = {}  # { "filename": {"hash": "...", "nodes": ["192.168.1.X", ...] } }  
ACTIVE_DATANODES = [] 
def handle_client(conn, addr):    
    try:        
        data = conn.recv(1024).decode('utf-8')        
        if not data: return        
        req = json.loads(data)        
        action = req.get("action")        
        
        if action == "register_node":            
            node_ip = req["ip"]            
            if node_ip not in ACTIVE_DATANODES: ACTIVE_DATANODES.append(node_ip)            
            res = {"status": "OK", "msg": f"DataNode {node_ip} registrado"}        
        elif action == "register_file":            
            METADATA_DB[req["filename"]] = {"hash": req["hash"], "nodes": list(ACTIVE_DATANODES)}            
            res = {"status": "OK", "nodes": list(ACTIVE_DATANODES)}        
        elif action == "lookup":            
            if req["filename"] in METADATA_DB:                
                res = {"status": "OK", "info": METADATA_DB[req["filename"]]}            
            else:                
                res = {"status": "ERROR", "msg": "Archivo no encontrado"}      
        else:            
            res = {"status": "ERROR", "msg": "Accion no soportada"}        
        conn.send(json.dumps(res).encode('utf-8'))    
    finally:        
        conn.close() 
    
    
def start_server():    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    server.bind(('0.0.0.0', 5000))    
    server.listen(10)    
    print("[NAMENODE] Servidor activo en puerto 5000. Esperando nodos y clientes...")    
    while True:        
        conn, addr = server.accept()        
        threading.Thread(target=handle_client, args=(conn, addr)).start() 
        
if __name__ == "__main__":    
    start_server()
    
    