class Config:
    DIR = "WorkDirectory"
    SEPARATOR_DIR = '\\'
    COMMANDS = {
        'ls': 'showDirectories',
        'dir': 'showDirectories',
        'cd': 'moveToDirectory',
        'mkdir': 'createDirectory',
        'rmdir': 'deleteDirectory',
        'touch': 'createFile',
        'write': 'writeToFile',
        'cat': 'readFile',
        'rm': 'deleteFile',
        'copy': 'copyFile',
        'move': 'moveFile',
        'rename': 'renameFile',
        'pwd': 'pwd'
    }