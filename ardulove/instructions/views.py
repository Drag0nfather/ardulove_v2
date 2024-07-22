from django.shortcuts import render, get_object_or_404

from .models import Instruction, InstructionTag


def instruction_main(request):
    tag_id = request.GET.get('tag')
    if tag_id:
        instructions = Instruction.objects.filter(tags__id=tag_id).order_by('-id')
    else:
        instructions = Instruction.objects.all().order_by('-id')

    tags = InstructionTag.objects.all()
    return render(request, 'instructions/instructions.html', {'instructions': instructions, 'tags': tags})


def instruction_detail(request, instruction_id):
    instruction = get_object_or_404(Instruction, pk=instruction_id)
    return render(request, 'instructions/instruction_detail.html', {'instruction': instruction})
