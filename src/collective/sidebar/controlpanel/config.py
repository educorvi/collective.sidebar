
from collective.sidebar import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


positionTerms = [
    SimpleTerm(
        value="start",
        title=_("left_in_ltr", default="Left (in LTR)"),
    ),
    SimpleTerm(
        value="end",
        title=_("right_in_ltr", default="Right (in LTR)"),
    ),
]

PositionVocabulary = SimpleVocabulary(positionTerms)
