# coding: utf-8
import collections
import zope.interface
import zope.cachedescriptors.property
import zope.component
import zope.contentprovider.interfaces
import zope.viewlet.interfaces
import grok
import ith.interfaces
import ith.permission
import ith.browser.layout


grok.templatedir('templates')


class Debugger(grok.Viewlet):
    grok.viewletmanager(ith.browser.layout.BelowFooter)
    grok.context(zope.interface.Interface)
    grok.layer(zope.publisher.interfaces.browser.IBrowserRequest)
    grok.require(ith.permission.PUBLIC)
    grok.name('debugger')
    grok.template('debugger')

    def available(self):
        return ith.util.in_dev_mode()

    @property
    def inspect(self):
        return ('debug' in self.request.form and
                self.request.form.get('debug') != '0')

    def maybe_start_pdb(self):
        if 'pdb' not in self.request.form:
            return
        if self.request.get('SERVER_PORT') == '8080':
            # assume foreground paster process, direct pdb
            import pdb
            pdb.set_trace()
        else:
            # start rpdb on localhost 1337
            import md.testing
            md.testing.debug()
        return 'pdb finished'

    @property
    def context_info(self):
        info = collections.OrderedDict()
        info['class'] = repr(self.context.__class__)
        info['name'] = repr(self.context.__name__)
        info['parent'] = repr(self.context.__parent__)
        return info

    @property
    def context_provides(self):
        return sorted([repr(x) for x in self.context.__provides__])

    @property
    def context_bases(self):
        return sorted([repr(x) for x in self.context.__class__.__bases__])

    @property
    def view_info(self):
        return self.view_component_info(self.view)

    @property
    def view_bases(self):
        return [repr(x) for x in self.view.__class__.__bases__]

    @property
    def viewlet_managers(self):
        self.viewlets = {}
        managers = zope.component.getAdapters(
            (self.context, self.request, self.view),
            zope.viewlet.interfaces.IViewletManager)
        info = {}
        for (name, manager) in managers:
            manager_info = self.view_component_info(manager)
            self.viewlets[name] = self._viewlets(manager)
            info[name] = manager_info
        return collections.OrderedDict(sorted(info.items()))

    def _viewlets(self, manager):
        viewlets = zope.component.getAdapters(
            (self.context, self.request, self.view, manager),
            zope.viewlet.interfaces.IViewlet)
        info = {name: self.view_component_info(viewlet)
                for (name, viewlet) in viewlets}
        return collections.OrderedDict(sorted(info.items()))

    @property
    def content_providers(self):
        """All content providers which are not also viewlet managers"""
        providers = zope.component.getAdapters(
            (self.context, self.request, self.view),
            zope.contentprovider.interfaces.IContentProvider)
        IViewletManager = zope.viewlet.interfaces.IViewletManager
        info = {name: self.view_component_info(provider)
                for (name, provider) in providers
                if not IViewletManager.providedBy(provider)}
        return collections.OrderedDict(sorted(info.items()))

    @property
    def request_info(self):
        info = collections.OrderedDict()
        info['annotations'] = self.request.annotations
        info['form'] = self.request.form
        info['principal'] = self.request.principal
        return info

    @property
    def request_items(self):
        info = collections.OrderedDict()
        for key in sorted(self.request.keys()):
            info[key] = self.request[key]
        return info

    def view_component_info(self, component):
        info = collections.OrderedDict()
        info['class'] = repr(component.__class__)
        try:
            info['name'] = repr(component.__view_name__)
        except AttributeError:
            pass
        try:
            info['template'] = repr(component.template)
        except AttributeError:
            pass
        try:
            info['layout'] = repr(component.layout)
            info['layout.template'] = repr(component.layout.template)
        except AttributeError:
            pass
        for key in sorted(dir(component)):
            if 'directive' in key:
                info[key] = getattr(component, key)
        return info
