from cloudify.decorators import workflow
from cloudify.workflows import ctx
from cloudify.workflows import tasks as workflow_tasks
from utils import set_state_task
from utils import operation_task
from utils import link_tasks
from utils import CustomContext
from utils import generate_native_node_workflows


@workflow
def a4c_install(**kwargs):
    graph = ctx.graph_mode()
    custom_context = CustomContext(ctx)
    ctx.internal.send_workflow_event(
        event_type='workflow_started',
        message="Starting A4C generated '{0}' workflow execution".format(ctx.workflow_id))
    _a4c_install(ctx, graph, custom_context)
    return graph.execute()


@workflow
def a4c_uninstall(**kwargs):
    graph = ctx.graph_mode()
    custom_context = CustomContext(ctx)
    ctx.internal.send_workflow_event(
        event_type='workflow_started',
        message="Starting A4C generated '{0}' workflow execution".format(ctx.workflow_id))
    _a4c_uninstall(ctx, graph, custom_context)
    return graph.execute()


def _a4c_install(ctx, graph, custom_context):
    #  following code can be pasted in src/test/python/workflows/tasks.py for simulation
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'starting', 'PHP_starting', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'started', 'Wordpress_started', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'configuring', 'Mysql_configuring', custom_context)
    operation_task(ctx, graph, 'Mysql', 'cloudify.interfaces.lifecycle.create', 'create_Mysql', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'initial', 'Apache_initial', custom_context)
    operation_task(ctx, graph, 'Mysql', 'cloudify.interfaces.lifecycle.configure', 'configure_Mysql', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'configured', 'Wordpress_configured', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'starting', 'Wordpress_starting', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'created', 'Mysql_created', custom_context)
    custom_context.register_native_delegate_wf_step('DataBase', 'DataBase_install')
    operation_task(ctx, graph, 'PHP', 'cloudify.interfaces.lifecycle.start', 'start_PHP', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'starting', 'Apache_starting', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'configuring', 'PHP_configuring', custom_context)
    custom_context.register_native_delegate_wf_step('Server', 'Server_install')
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'created', 'PHP_created', custom_context)
    operation_task(ctx, graph, 'Wordpress', 'cloudify.interfaces.lifecycle.start', 'start_Wordpress', custom_context)
    operation_task(ctx, graph, 'Apache', 'cloudify.interfaces.lifecycle.configure', 'configure_Apache', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'creating', 'Mysql_creating', custom_context)
    operation_task(ctx, graph, 'Apache', 'cloudify.interfaces.lifecycle.create', 'create_Apache', custom_context)
    custom_context.register_native_delegate_wf_step('InternalNetwork', 'InternalNetwork_install')
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'initial', 'Wordpress_initial', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'configured', 'Apache_configured', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'started', 'PHP_started', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'configuring', 'Wordpress_configuring', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'creating', 'PHP_creating', custom_context)
    operation_task(ctx, graph, 'Wordpress', 'cloudify.interfaces.lifecycle.configure', 'configure_Wordpress', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'starting', 'Mysql_starting', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'configured', 'Mysql_configured', custom_context)
    custom_context.register_native_delegate_wf_step('NetPub', 'NetPub_install')
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'creating', 'Apache_creating', custom_context)
    operation_task(ctx, graph, 'PHP', 'cloudify.interfaces.lifecycle.create', 'create_PHP', custom_context)
    operation_task(ctx, graph, 'Apache', 'cloudify.interfaces.lifecycle.start', 'start_Apache', custom_context)
    operation_task(ctx, graph, 'PHP', 'cloudify.interfaces.lifecycle.configure', 'configure_PHP', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'started', 'Mysql_started', custom_context)
    operation_task(ctx, graph, 'Wordpress', 'cloudify.interfaces.lifecycle.create', 'create_Wordpress', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'creating', 'Wordpress_creating', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'initial', 'Mysql_initial', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'created', 'Apache_created', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'started', 'Apache_started', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'created', 'Wordpress_created', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'configuring', 'Apache_configuring', custom_context)
    operation_task(ctx, graph, 'Mysql', 'cloudify.interfaces.lifecycle.start', 'start_Mysql', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'initial', 'PHP_initial', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'configured', 'PHP_configured', custom_context)
    generate_native_node_workflows(ctx, graph, custom_context, 'install')
    link_tasks(graph, 'PHP_starting', 'PHP_configured', custom_context)
    link_tasks(graph, 'Wordpress_started', 'start_Wordpress', custom_context)
    link_tasks(graph, 'Mysql_configuring', 'Wordpress_created', custom_context)
    link_tasks(graph, 'Mysql_configuring', 'Mysql_created', custom_context)
    link_tasks(graph, 'create_Mysql', 'Mysql_creating', custom_context)
    link_tasks(graph, 'Apache_initial', 'Server_install', custom_context)
    link_tasks(graph, 'configure_Mysql', 'Mysql_configuring', custom_context)
    link_tasks(graph, 'Wordpress_configured', 'configure_Wordpress', custom_context)
    link_tasks(graph, 'Wordpress_starting', 'Wordpress_configured', custom_context)
    link_tasks(graph, 'Mysql_created', 'create_Mysql', custom_context)
    link_tasks(graph, 'start_PHP', 'PHP_starting', custom_context)
    link_tasks(graph, 'Apache_starting', 'Apache_configured', custom_context)
    link_tasks(graph, 'PHP_configuring', 'PHP_created', custom_context)
    link_tasks(graph, 'PHP_configuring', 'Wordpress_created', custom_context)
    link_tasks(graph, 'PHP_created', 'create_PHP', custom_context)
    link_tasks(graph, 'start_Wordpress', 'Wordpress_starting', custom_context)
    link_tasks(graph, 'configure_Apache', 'Apache_configuring', custom_context)
    link_tasks(graph, 'Mysql_creating', 'Mysql_initial', custom_context)
    link_tasks(graph, 'create_Apache', 'Apache_creating', custom_context)
    link_tasks(graph, 'Wordpress_initial', 'Apache_started', custom_context)
    link_tasks(graph, 'Apache_configured', 'configure_Apache', custom_context)
    link_tasks(graph, 'PHP_started', 'start_PHP', custom_context)
    link_tasks(graph, 'Wordpress_configuring', 'Mysql_started', custom_context)
    link_tasks(graph, 'Wordpress_configuring', 'PHP_started', custom_context)
    link_tasks(graph, 'Wordpress_configuring', 'Wordpress_created', custom_context)
    link_tasks(graph, 'PHP_creating', 'PHP_initial', custom_context)
    link_tasks(graph, 'configure_Wordpress', 'Wordpress_configuring', custom_context)
    link_tasks(graph, 'Mysql_starting', 'Mysql_configured', custom_context)
    link_tasks(graph, 'Mysql_configured', 'configure_Mysql', custom_context)
    link_tasks(graph, 'Apache_creating', 'Apache_initial', custom_context)
    link_tasks(graph, 'create_PHP', 'PHP_creating', custom_context)
    link_tasks(graph, 'start_Apache', 'Apache_starting', custom_context)
    link_tasks(graph, 'configure_PHP', 'PHP_configuring', custom_context)
    link_tasks(graph, 'Mysql_started', 'start_Mysql', custom_context)
    link_tasks(graph, 'create_Wordpress', 'Wordpress_creating', custom_context)
    link_tasks(graph, 'Wordpress_creating', 'Wordpress_initial', custom_context)
    link_tasks(graph, 'Mysql_initial', 'DataBase_install', custom_context)
    link_tasks(graph, 'Apache_created', 'create_Apache', custom_context)
    link_tasks(graph, 'Apache_started', 'start_Apache', custom_context)
    link_tasks(graph, 'Wordpress_created', 'create_Wordpress', custom_context)
    link_tasks(graph, 'Apache_configuring', 'Apache_created', custom_context)
    link_tasks(graph, 'start_Mysql', 'Mysql_starting', custom_context)
    link_tasks(graph, 'PHP_initial', 'Server_install', custom_context)
    link_tasks(graph, 'PHP_configured', 'configure_PHP', custom_context)


def _a4c_uninstall(ctx, graph, custom_context):
    #  following code can be pasted in src/test/python/workflows/tasks.py for simulation
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'stopping', 'PHP_stopping', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'deleting', 'Wordpress_deleting', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'stopped', 'Apache_stopped', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'deleted', 'Mysql_deleted', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'deleted', 'Apache_deleted', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'deleted', 'Wordpress_deleted', custom_context)
    custom_context.register_native_delegate_wf_step('InternalNetwork', 'InternalNetwork_uninstall')
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'deleting', 'Mysql_deleting', custom_context)
    custom_context.register_native_delegate_wf_step('NetPub', 'NetPub_uninstall')
    custom_context.register_native_delegate_wf_step('DataBase', 'DataBase_uninstall')
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'deleting', 'Apache_deleting', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'stopped', 'Wordpress_stopped', custom_context)
    custom_context.add_customized_wf_node('Apache')
    set_state_task(ctx, graph, 'Apache', 'stopping', 'Apache_stopping', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'deleting', 'PHP_deleting', custom_context)
    custom_context.register_native_delegate_wf_step('Server', 'Server_uninstall')
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'stopped', 'PHP_stopped', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'stopped', 'Mysql_stopped', custom_context)
    custom_context.add_customized_wf_node('Wordpress')
    set_state_task(ctx, graph, 'Wordpress', 'stopping', 'Wordpress_stopping', custom_context)
    custom_context.add_customized_wf_node('PHP')
    set_state_task(ctx, graph, 'PHP', 'deleted', 'PHP_deleted', custom_context)
    custom_context.add_customized_wf_node('Mysql')
    set_state_task(ctx, graph, 'Mysql', 'stopping', 'Mysql_stopping', custom_context)
    generate_native_node_workflows(ctx, graph, custom_context, 'uninstall')
    link_tasks(graph, 'Wordpress_deleting', 'Wordpress_stopped', custom_context)
    link_tasks(graph, 'Apache_stopped', 'Apache_stopping', custom_context)
    link_tasks(graph, 'Mysql_deleted', 'Mysql_deleting', custom_context)
    link_tasks(graph, 'Apache_deleted', 'Apache_deleting', custom_context)
    link_tasks(graph, 'Wordpress_deleted', 'Wordpress_deleting', custom_context)
    link_tasks(graph, 'Mysql_deleting', 'Mysql_stopped', custom_context)
    link_tasks(graph, 'DataBase_uninstall', 'Mysql_deleted', custom_context)
    link_tasks(graph, 'Apache_deleting', 'Apache_stopped', custom_context)
    link_tasks(graph, 'Wordpress_stopped', 'Wordpress_stopping', custom_context)
    link_tasks(graph, 'Apache_stopping', 'Wordpress_deleted', custom_context)
    link_tasks(graph, 'PHP_deleting', 'PHP_stopped', custom_context)
    link_tasks(graph, 'Server_uninstall', 'Apache_deleted', custom_context)
    link_tasks(graph, 'Server_uninstall', 'PHP_deleted', custom_context)
    link_tasks(graph, 'PHP_stopped', 'PHP_stopping', custom_context)
    link_tasks(graph, 'Mysql_stopped', 'Mysql_stopping', custom_context)
    link_tasks(graph, 'PHP_deleted', 'PHP_deleting', custom_context)


#following code can be pasted in src/test/python/workflows/context.py for simulation
#def _build_nodes(ctx):
    #types = []
    #types.append('alien.nodes.Apache')
    #types.append('tosca.nodes.WebServer')
    #types.append('tosca.nodes.SoftwareComponent')
    #types.append('tosca.nodes.Root')
    #node_Apache = _build_node(ctx, 'Apache', types, 1)
    #types = []
    #types.append('alien.nodes.openstack.Compute')
    #types.append('tosca.nodes.Compute')
    #types.append('tosca.nodes.Root')
    #node_DataBase = _build_node(ctx, 'DataBase', types, 1)
    #types = []
    #types.append('alien.nodes.PHP')
    #types.append('tosca.nodes.SoftwareComponent')
    #types.append('tosca.nodes.Root')
    #node_PHP = _build_node(ctx, 'PHP', types, 1)
    #types = []
    #types.append('alien.nodes.Wordpress')
    #types.append('tosca.nodes.WebApplication')
    #types.append('tosca.nodes.Root')
    #node_Wordpress = _build_node(ctx, 'Wordpress', types, 1)
    #types = []
    #types.append('alien.nodes.openstack.PrivateNetwork')
    #types.append('alien.nodes.PrivateNetwork')
    #types.append('tosca.nodes.Network')
    #types.append('tosca.nodes.Root')
    #node_InternalNetwork = _build_node(ctx, 'InternalNetwork', types, 1)
    #types = []
    #types.append('alien.nodes.openstack.PublicNetwork')
    #types.append('alien.nodes.PublicNetwork')
    #types.append('tosca.nodes.Network')
    #types.append('tosca.nodes.Root')
    #node_NetPub = _build_node(ctx, 'NetPub', types, 1)
    #types = []
    #types.append('alien.nodes.openstack.Compute')
    #types.append('tosca.nodes.Compute')
    #types.append('tosca.nodes.Root')
    #node_Server = _build_node(ctx, 'Server', types, 1)
    #types = []
    #types.append('alien.nodes.Mysql')
    #types.append('tosca.nodes.Database')
    #types.append('tosca.nodes.Root')
    #node_Mysql = _build_node(ctx, 'Mysql', types, 1)
    #_add_relationship(node_Apache, node_Server)
    #_add_relationship(node_DataBase, node_InternalNetwork)
    #_add_relationship(node_PHP, node_Server)
    #_add_relationship(node_Wordpress, node_PHP)
    #_add_relationship(node_Wordpress, node_Apache)
    #_add_relationship(node_Wordpress, node_Mysql)
    #_add_relationship(node_Server, node_NetPub)
    #_add_relationship(node_Server, node_InternalNetwork)
    #_add_relationship(node_Mysql, node_DataBase)
