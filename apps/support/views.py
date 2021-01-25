from apps.commons.mixins.commons import CustomListView, CustomDetailView, \
    CustomExportView, CustomCreateView, CustomAjaxCreateView
from .models import Ticket, Chat
from .forms import SupportChatForm
from django.urls import reverse_lazy


class SupportListView(CustomListView):
    model = Ticket
    template_name = 'support/support.html'


class SupportChatView(CustomCreateView):
    model = Chat
    template_name = 'support/reply.html'
    form_class = SupportChatForm

    def form_valid(self, form, **kwargs):
        form.instance.ticket = Ticket.objects.filter(
            id=self.kwargs.get(self.pk_url_kwarg)).first()
        form.instance.sender = self.request.user
        return super(SupportChatView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['pk'] = self.kwargs.get(self.pk_url_kwarg)
        context['ticket'] = Ticket.objects.filter(
            id=context['pk']).first()
        context['support_chat'] = Chat.objects.filter(
            ticket__id=context['pk'])
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('support:support-reply', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
