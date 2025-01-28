import os
from flask_assets import Bundle

def recursive_flatten_iterator(d):
    for _, v in d.items():
        if isinstance(v, list):
            yield v
        elif isinstance(v, dict):
            yield from recursive_flatten_iterator(v)

def register_bundles(assets, bundles):
    for x in recursive_flatten_iterator(bundles):
        for bundle in x:
            register_bundle(assets, bundle)


def register_bundle(assets, bundle):
    assets.register(bundle['name'], bundle['instance'])
    return f'Budle {bundle["name"]} registered'

def get_bundle(route, template, ext, paths, type=False):
    if route and template and ext:
        return {
            'instance' : Bundle(*paths, output = get_path(route, template, ext, type), filters = get_filters(ext)),
            'name':get_filename(route, template, ext, type),
            'dir' : os.getcwd()
        } 

def get_filename(route, template, ext, type):
    if type:
        return f'{route}_{template}_{ext}_defer'
    else:
        return f'{route}_{template}_{ext}'
    
def get_path(route, template, ext, type):
    if type:
        return f'gen/{route}/{template}/defer.{ext}'
    else:
        return f'gen/{route}/{template}/main.{ext}'
        
def get_filters(ext):
    return f'{ext}min'

bundles = {
    'css' : [ get_bundle('main', 'index', 'css', ['css/blocks/scene.css',])],
    # 'js':[
    #     get_bundle('main', 'base', 'js', ['js/base.js', ])
    # ]
}