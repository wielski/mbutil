import os, shutil
import sys
import json
from nose import with_setup
from mbutil import mbtiles_to_disk, disk_to_mbtiles

def clear_data():
    try: shutil.rmtree('test/output')
    except Exception: pass

@with_setup(clear_data, clear_data)
def test_mbtiles_to_disk():
    mbtiles_to_disk('test/data/one_tile.mbtiles', 'test/output')
    assert os.path.exists('test/output/0/0/0.png')
    assert os.path.exists('test/output/metadata.json')

@with_setup(clear_data, clear_data)
def test_mbtiles_to_disk_and_back():
    mbtiles_to_disk('test/data/one_tile.mbtiles', 'test/output')
    assert os.path.exists('test/output/0/0/0.png')
    disk_to_mbtiles('test/output/', 'test/output/one.mbtiles')
    assert os.path.exists('test/output/one.mbtiles')

@with_setup(clear_data, clear_data)
def test_utf8grid_mbtiles_to_disk():
    mbtiles_to_disk('test/data/utf8grid.mbtiles', 'test/output')
    assert os.path.exists('test/output/0/0/0.grid.json')
    assert os.path.exists('test/output/0/0/0.png')
    assert os.path.exists('test/output/metadata.json')

@with_setup(clear_data, clear_data)
def test_utf8grid_disk_to_mbtiles():
    os.mkdir('test/output')
    mbtiles_to_disk('test/data/utf8grid.mbtiles', 'test/output/original', callback=None)
    disk_to_mbtiles('test/output/original/', 'test/output/imported.mbtiles')
    mbtiles_to_disk('test/output/imported.mbtiles', 'test/output/imported', callback=None)
    assert os.path.exists('test/output/imported/0/0/0.grid.json')
    original = json.load(open('test/output/original/0/0/0.grid.json'))
    imported = json.load(open('test/output/imported/0/0/0.grid.json'))
    assert original['data']['77'] == imported['data']['77'] == {u'ISO_A2': u'FR'}

@with_setup(clear_data, clear_data)
def test_mbtiles_to_disk_utfgrid_callback():
    os.mkdir('test/output')
    callback = {}
    for c in ['null', 'foo']:
        mbtiles_to_disk('test/data/utf8grid.mbtiles', 'test/output/%s' % c, callback=c)
        f = open('test/output/%s/0/0/0.grid.json' % c)
        callback[c] = f.read().split('{')[0]
        f.close()
    assert callback['foo'] == 'foo('
    assert callback['null'] == ''

@with_setup(clear_data, clear_data)
def test_disk_to_mbtiles_zyx():
    os.mkdir('test/output')
    disk_to_mbtiles('test/data/tiles/zyx', 'test/output/zyx.mbtiles', scheme='zyx', format='png')
    mbtiles_to_disk('test/output/zyx.mbtiles', 'test/output/tiles', callback=None)
    assert os.path.exists('test/output/tiles/3/1/5.png')

@with_setup(clear_data, clear_data)
def test_disk_to_mbtiles_no_extension_zyx():
    os.mkdir('test/output')
    disk_to_mbtiles('test/data/tiles-no-extension/zyx', 'test/output/zyx-no-extension.mbtiles', scheme='zyx', format='png', no_extension=True)
    mbtiles_to_disk('test/output/zyx-no-extension.mbtiles', 'test/output/tiles-no-extension', callback=None)
    assert os.path.exists('test/output/tiles-no-extension/3/1/5.png')
