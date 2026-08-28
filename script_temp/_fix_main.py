import sys
with open('app/main.py', 'a', encoding='utf-8') as f:
    f.write('\n\nif __name__ == \
__main__\:\n    import uvicorn\n    uvicorn.run(app, host=\0.0.0.0\, port=8056)\n')
