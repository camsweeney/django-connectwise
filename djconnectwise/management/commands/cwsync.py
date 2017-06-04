from collections import OrderedDict

from djconnectwise import sync, api

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

OPTION_NAME = 'connectwise_object'


class Command(BaseCommand):
    help = _('Synchronize the specified object with the Connectwise API')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This can be replaced with a single instantiation of an OrderedDict
        # using kwargs in Python 3.6. But we need Python 3.5 compatibility for
        # now.
        # See https://www.python.org/dev/peps/pep-0468/.
        synchronizers = (
            ('member', sync.MemberSynchronizer, _('Member')),
            ('board', sync.BoardSynchronizer, _('Board')),
            ('team', sync.TeamSynchronizer, _('Team')),
            ('board_status', sync.BoardStatusSynchronizer, _('Board Status')),
            ('priority', sync.PrioritySynchronizer, _('Priority')),
            ('project', sync.ProjectSynchronizer, _('Project')),
            ('company_status', sync.CompanyStatusSynchronizer,
                _('Company Status')),
            ('company', sync.CompanySynchronizer, _('Company')),
            ('location', sync.LocationSynchronizer, _('Location')),
            ('opportunity_status', sync.OpportunityStatusSynchronizer,
                _('Opportunity Status')),
            ('ticket', sync.TicketSynchronizer, _('Ticket')),
        )
        self.synchronizer_map = OrderedDict()
        for name, syncronizer, obj_name in synchronizers:
            self.synchronizer_map[name] = (syncronizer, obj_name)

    def add_arguments(self, parser):
        parser.add_argument(OPTION_NAME, nargs='?', type=str)
        parser.add_argument('--reset',
                            action='store_true',
                            dest='reset',
                            default=False)

    def sync_by_class(self, sync_class, obj_name, reset=False):
        synchronizer = sync_class()

        created_count, updated_count, deleted_count = synchronizer.sync(
            reset=reset)

        msg = _('{} Sync Summary - Created: {}, Updated: {}')
        fmt_msg = msg.format(obj_name, created_count, updated_count)

        if reset:
            msg = _('{} Sync Summary - Created: {}, Updated: {}, Deleted: {}')
            fmt_msg = msg.format(obj_name, created_count, updated_count,
                                 deleted_count)

        self.stdout.write(fmt_msg)

    def handle(self, *args, **options):
        sync_classes = []
        connectwise_object_arg = options[OPTION_NAME]
        reset_option = options.get('reset', False)

        if connectwise_object_arg:
            object_arg = connectwise_object_arg
            sync_tuple = self.synchronizer_map.get(object_arg)

            if sync_tuple:
                sync_classes.append(sync_tuple)
            else:
                msg = _('Invalid CW object, choose one of the following: \n{}')
                options_txt = ', '.join(self.synchronizer_map.keys())
                msg = msg.format(options_txt)
                raise CommandError(msg)
        else:
            sync_classes = self.synchronizer_map.values()

        failed_classes = 0
        error_messages = ''

        num_synchronizers = len(self.synchronizer_map)
        has_ticket_sync = 'ticket' in self.synchronizer_map
        if reset_option and num_synchronizers and has_ticket_sync:
            sync_classes = list(sync_classes)
            sync_classes.reverse()
            # need to move ticket synchronizer to the tail of the list
            sync_classes.append(sync_classes.pop(0))

        for sync_class, obj_name in sync_classes:
            try:
                self.sync_by_class(sync_class, obj_name, reset=reset_option)

            except api.ConnectWiseAPIError as e:
                msg = 'Failed to sync {}: {}'.format(obj_name, e)
                self.stderr.write(msg)
                error_messages += '{}\n'.format(msg)
                failed_classes += 1

        if failed_classes > 0:
            msg = '{} class{} failed to sync.\n'.format(
                failed_classes,
                '' if failed_classes == 1 else 'es',
            )
            msg += 'Errors:\n'
            msg += error_messages
            raise CommandError(msg)
