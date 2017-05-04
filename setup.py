from setuptools import setup, find_packages

version = '1.0.dev0'

setup(
    name='introspect',
    version=version,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grok',
        'grokcore.chameleon',
        'ith >= 8.5.dev0',
        'md.testing',
        'setuptools',
        'zope.cachedescriptors',
        'zope.component',
        'zope.interface',
        'zope.location',
        'zope.proxy',
        'zope.schema',
        'zope.security',
        'zope.traversing',
        ],
    entry_points={},
    extras_require={
        'test': [
            'zope.testing',
            'md.testing[browser]'
        ]},
    message_extractors={})
