##############################################################################
# VoiceCode, a programming-by-voice environment
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# (C)2001, National Research Council of Canada
#
##############################################################################

"""State information for an external source buffer connected to
VoiceCode via a messaging protocol."""

import messaging, sb_services, SourceBuffMessaging

class SourceBuffEmacs(SourceBuffMessaging.SourceBuffMessaging):
    
    """Interface to a buffer of the Emacs editor.
    
    **INSTANCE ATTRIBUTES**

    [SB_ServiceLang] *lang_srv* -- Language service used to know the
    programming language of a source file.
    
    Note that the *app* attribute (defined in [SourceBuff])
    needs to be a subclass of [AppStateEmacs]

    **CLASS ATTRIBUTES**
    
    *none* --

    ..[SourceBuff] file:///./SourceBuff.SourceBuff.py
    ..[AppStateEmacs] file:///./AppStateEmacs.AppStateEmacs.html"""
    
    def __init__(self, **attrs):
        self.init_attrs({'lang_srv': sb_services.SB_ServiceLang(buff=self)})
        self.deep_construct(SourceBuffEmacs,
                            {},
                            attrs
                            )
    def cleanup(self):
        """method to cleanup circular references by cleaning up 
	any children, and then removing the reference to the parent

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        self.lang_srv.cleanup()
	SourceBuffMessaging.SourceBuffMessaging.cleanup(self)

    def language_name(self):
        """Returns the name of the language a file is written in.

        This would be better handled at the Emacs level, but I haven't
        figured out how to find the language of a buffer in Emacs (AD).
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**
        
        *STR* -- the name of the language
        """

        return self.lang_srv.language_name()
