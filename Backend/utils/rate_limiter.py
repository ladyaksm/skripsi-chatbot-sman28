import redis
from flask import request, jsonify

# Redis khusus buat rate limit (DB berbeda biar ga tabrakan)
r = redis.Redis(host="localhost", port=6379, db=3)

def rate_limit(max_requests=5, window_seconds=60):
    def decorator(func):
        def wrapper(*args, **kwargs):

            if request.method == "OPTIONS":
                return jsonify({"status": "ok"}), 200

            ip = request.remote_addr
            key = f"rate:{ip}"

            # ambil jumlah request sebelumnya
            reqs = r.get(key)

            if reqs:
                reqs = int(reqs)

                # kalau udah melewati batas
                if reqs >= max_requests:
                    # Ambil sisa waktu TTL
                    ttl = r.ttl(key)
                    
                    return jsonify({
                          "error": f"Maaf ya, kamu kebanyakan ngirim pertanyaan",
                          "retry_after": ttl,
                          "message": f"Coba lagi dalam {ttl} detik lagi yaa~"
                          }), 429

                # tambah counter
                r.incr(key)

            else:
                # request pertama → bikin key + TTL
                r.set(key, 1, ex=window_seconds)

            return func(*args, **kwargs)

        return wrapper
    return decorator
