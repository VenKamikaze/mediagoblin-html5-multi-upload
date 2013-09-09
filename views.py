# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Created by Mick Saunders, based off normal submit form views.py

from mediagoblin import messages
import mediagoblin.mg_globals as mg_globals
from os.path import splitext

import logging
import uuid

_log = logging.getLogger(__name__)


from mediagoblin.tools.text import convert_to_tag_list_of_dicts
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.response import render_to_response, redirect
from mediagoblin.decorators import require_active_login
from mediagoblin.submit import forms as submit_forms
from mediagoblin.messages import add_message, SUCCESS
from mediagoblin.media_types import sniff_media, \
    InvalidFileType, FileTypeNotSupported
from mediagoblin.submit.lib import check_file_field, prepare_queue_task, \
    run_process_media, new_upload_entry

from mediagoblin.notifications import add_comment_subscription


@require_active_login
def multi_submit_start(request):
  """
  First view for submitting a file.
  """
  submit_form = submit_forms.SubmitStartForm(request.form, license=request.user.license_preference)
  filecount = 0
  if request.method == 'POST' and submit_form.validate():
    if not check_file_field(request, 'file'):
      submit_form.file.errors.append(_(u'You must provide at least one file.'))
    else:
      for submitted_file in request.files.getlist('file'):
        try:
          if not submitted_file.filename:
            # MOST likely an invalid file
            continue # Skip the rest of the loop for this file
          else:
            filename = submitted_file.filename
            _log.info("html5-multi-upload: Got filename: %s" % filename)
    
            # If the filename contains non ascii generate a unique name
            if not all(ord(c) < 128 for c in filename):
              filename = unicode(uuid.uuid4()) + splitext(filename)[-1]
    
            # Sniff the submitted media to determine which
            # media plugin should handle processing
            media_type, media_manager = sniff_media(
              submitted_file)
    
            # create entry and save in database
            entry = new_upload_entry(request.user)
            entry.media_type = unicode(media_type)
            entry.title = (
              unicode(submit_form.title.data)
              or unicode(splitext(submitted_file.filename)[0]))
    
            entry.description = unicode(submit_form.description.data)
    
            entry.license = unicode(submit_form.license.data) or None
    
            # Process the user's folksonomy "tags"
            entry.tags = convert_to_tag_list_of_dicts(
              submit_form.tags.data)
    
            # Generate a slug from the title
            entry.generate_slug()
    
            queue_file = prepare_queue_task(request.app, entry, filename)
    
            with queue_file:
              queue_file.write(submitted_file.stream.read())
    
            # Save now so we have this data before kicking off processing
            entry.save()
    
            # Pass off to async processing
            #
            # (... don't change entry after this point to avoid race
            # conditions with changes to the document via processing code)
            feed_url = request.urlgen(
              'mediagoblin.user_pages.atom_feed',
              qualified=True, user=request.user.username)
            run_process_media(entry, feed_url)
    
            add_comment_subscription(request.user, entry)
            filecount = filecount + 1

        except Exception as e:
          '''
          This section is intended to catch exceptions raised in
          mediagoblin.media_types
          '''
          if isinstance(e, InvalidFileType) or isinstance(e, FileTypeNotSupported):
            submit_form.file.errors.append(e)
          else:
            raise

      add_message(request, SUCCESS, _('Woohoo! Submitted %d Files!' % filecount))
      return redirect(request, "mediagoblin.user_pages.user_home",
              user=request.user.username)

  return render_to_response(
    request,
    'start.html',
    {'multi_submit_form': submit_form})

